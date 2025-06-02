import faiss
import numpy as np
import pickle
import sys
import json
import argparse
import os

# EMBEDDING_DIM needs to be verified for nomic-embed-text.
# Common values are 768, 512, etc. Let's use 768 as a placeholder.
EMBEDDING_DIM = 768

def init_index(index_path, metadata_path, dim=EMBEDDING_DIM):
    """
    Initializes a new FAISS index and a metadata file.
    """
    print(f"Attempting to initialize FAISS index at: {index_path} with dimension {dim}")
    print(f"Attempting to initialize metadata file at: {metadata_path}")

    if os.path.exists(index_path) or os.path.exists(metadata_path):
        print(f"Error: Index '{index_path}' or metadata '{metadata_path}' already exists. Please remove them first or use a different path.")
        return

    try:
        index = faiss.IndexFlatL2(dim)
        faiss.write_index(index, index_path)
        with open(metadata_path, 'wb') as f:
            pickle.dump([], f) # Initialize with an empty list for texts
        print(f"Successfully initialized FAISS index at: {index_path}")
        print(f"Successfully initialized metadata file at: {metadata_path}")
    except Exception as e:
        print(f"Error initializing index/metadata: {e}")

def add_embeddings(index_path, metadata_path, texts, embeddings_str):
    """
    Loads an existing FAISS index and metadata, adds new text chunks and their
    corresponding embeddings, and saves the updated index and metadata.
    'texts' should be a list of strings.
    'embeddings_str' should be a JSON string representing a list of lists (embeddings).
    """
    print(f"Attempting to add embeddings to FAISS index: {index_path}")
    print(f"Using metadata file: {metadata_path}")
    print(f"Texts to add: {texts}")
    # print(f"Embeddings string to add: {embeddings_str}") # Can be very long

    if not os.path.exists(index_path) or not os.path.exists(metadata_path):
        print(f"Error: Index '{index_path}' or metadata '{metadata_path}' not found. Please initialize first.")
        return

    try:
        # Load index
        index = faiss.read_index(index_path)
        print(f"Loaded FAISS index. Current ntotal: {index.ntotal}")

        # Load metadata
        with open(metadata_path, 'rb') as f:
            all_texts = pickle.load(f)
        print(f"Loaded metadata. Current number of texts: {len(all_texts)}")

        # Parse embeddings
        try:
            embeddings = np.array(json.loads(embeddings_str)).astype('float32')
            if embeddings.ndim != 2 or embeddings.shape[1] != index.d:
                print(f"Error: Embeddings have incorrect shape or dimension. Expected ({len(texts)}, {index.d}), got {embeddings.shape}")
                return
        except json.JSONDecodeError:
            print("Error: Could not decode JSON string for embeddings.")
            return
        except Exception as e:
            print(f"Error processing embeddings: {e}")
            return

        # Add to index and metadata
        index.add(embeddings)
        all_texts.extend(texts)

        # Save updated index and metadata
        faiss.write_index(index, index_path)
        with open(metadata_path, 'wb') as f:
            pickle.dump(all_texts, f)

        print(f"Successfully added {len(texts)} new embeddings and texts.")
        print(f"New FAISS index ntotal: {index.ntotal}")
        print(f"New metadata text count: {len(all_texts)}")

    except Exception as e:
        print(f"Error adding embeddings: {e}")

def search_index(index_path, metadata_path, query_embedding_str, k=5):
    """
    Loads the index and metadata, searches for the top_k most similar text chunks
    to the query_embedding, and returns these chunks.
    'query_embedding_str' should be a JSON string representing a single embedding vector.
    """
    print(f"Attempting to search FAISS index: {index_path}")
    print(f"Using metadata file: {metadata_path}")
    print(f"Searching for top {k} results.")
    # print(f"Query embedding string: {query_embedding_str}") # Can be long

    if not os.path.exists(index_path) or not os.path.exists(metadata_path):
        print(f"Error: Index '{index_path}' or metadata '{metadata_path}' not found. Please initialize first.")
        return

    try:
        index = faiss.read_index(index_path)
        if index.ntotal == 0:
            print("Warning: Index is empty. Search will yield no results.")
            return []

        with open(metadata_path, 'rb') as f:
            all_texts = pickle.load(f)

        try:
            query_embedding = np.array(json.loads(query_embedding_str)).astype('float32')
            if query_embedding.ndim == 1: # If it's a flat list, reshape
                 query_embedding = query_embedding.reshape(1, -1)
            if query_embedding.shape[1] != index.d:
                print(f"Error: Query embedding has incorrect dimension. Expected {index.d}, got {query_embedding.shape[1]}")
                return []
        except json.JSONDecodeError:
            print("Error: Could not decode JSON string for query embedding.")
            return []
        except Exception as e:
            print(f"Error processing query embedding: {e}")
            return []

        distances, indices = index.search(query_embedding, k)

        results = []
        print("Search Results (Indices, Distances):", indices, distances)
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx < len(all_texts):
                results.append({
                    "text": all_texts[idx],
                    "distance": float(distances[0][i]),
                    "index_position": int(idx)
                })
            else:
                print(f"Warning: Retrieved index {idx} is out of bounds for metadata (length {len(all_texts)}).")

        print(f"Retrieved {len(results)} results: {results}")
        # For n8n Execute Command, we typically print JSON to stdout
        print(json.dumps(results)) # Output results as JSON string
        return results

    except Exception as e:
        print(f"Error searching index: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Manage FAISS vector stores for RAG.")
    parser.add_argument('action', choices=['init', 'add', 'search'], help="Action to perform.")
    parser.add_argument('--index_path', default="vector_store/faiss_index.bin", help="Path to the FAISS index file.")
    parser.add_argument('--metadata_path', default="vector_store/metadata.pkl", help="Path to the metadata pickle file.")
    parser.add_argument('--dim', type=int, default=EMBEDDING_DIM, help="Dimension of embeddings for 'init' action.")

    # For 'add' action
    parser.add_argument('--texts', nargs='+', help="List of texts to add (for 'add' action). Should be passed as separate strings.")
    parser.add_argument('--embeddings', type=str, help="JSON string of embeddings to add (for 'add' action). Example: '[[0.1, 0.2], [0.3, 0.4]]'")

    # For 'search' action
    parser.add_argument('--query_embedding', type=str, help="JSON string of the query embedding (for 'search' action). Example: '[0.1, 0.2]'")
    parser.add_argument('--k', type=int, default=3, help="Number of results to retrieve (for 'search' action).")

    args = parser.parse_args()

    # Create directory for index and metadata if it doesn't exist
    index_dir = os.path.dirname(args.index_path)
    if index_dir and not os.path.exists(index_dir):
        os.makedirs(index_dir)
        print(f"Created directory: {index_dir}")

    if args.action == 'init':
        init_index(args.index_path, args.metadata_path, args.dim)
    elif args.action == 'add':
        if not args.texts or not args.embeddings:
            parser.error("--texts and --embeddings are required for 'add' action.")
        # In a real scenario, texts might come from a file or complex input
        # For CLI, argparse handles multiple strings for --texts.
        add_embeddings(args.index_path, args.metadata_path, args.texts, args.embeddings)
    elif args.action == 'search':
        if not args.query_embedding:
            parser.error("--query_embedding is required for 'search' action.")
        search_index(args.index_path, args.metadata_path, args.query_embedding, args.k)

if __name__ == '__main__':
    main()
