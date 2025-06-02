#!/usr/bin/env python3
"""
RAG Builder Script for Barry Sharp Pro Mover
Implements Phase 1 of the LANGFLOW-DEV-PLAN.md

This script:
1. Loads documents from the docs directory
2. Splits them into chunks
3. Creates embeddings using Ollama's nomic-embed-text model
4. Stores the embeddings in FAISS indexes in the vectorstore directory
"""

import os
import sys
import json
from pathlib import Path
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Try to import required packages
try:
    from langchain_community.document_loaders import DirectoryLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import OllamaEmbeddings
    import ollama
except ImportError as e:
    logger.error(f"Required package not found: {e}")
    logger.error("Please install required packages: pip install langchain langchain_community faiss-cpu")
    sys.exit(1)

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DOCS_DIR = PROJECT_ROOT / "docs"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

# Define knowledge base categories and their source directories
KB_CATEGORIES = {
    "design_kb": [DOCS_DIR / "design"],
    "art_kb": [DOCS_DIR / "art"],
    "code_kb": [DOCS_DIR / "code"],
    "dialogue_kb": [DOCS_DIR / "dialogue"],
    "music_kb": [DOCS_DIR / "music"],
    "shared_kb": [DOCS_DIR / "shared"],
    "qa_kb": [DOCS_DIR],  # QA can access all docs
}

def check_ollama_running():
    """Check if Ollama is running and the required model is available"""
    try:
        # Check if Ollama is running
        models = ollama.list()
        
        # Check if nomic-embed-text model is available
        model_names = [model.get('name') for model in models.get('models', [])]
        if 'nomic-embed-text' not in model_names:
            logger.warning("nomic-embed-text model not found in Ollama")
            logger.info("Pulling nomic-embed-text model...")
            ollama.pull('nomic-embed-text')
            logger.info("Model pulled successfully")
        return True
    except Exception as e:
        logger.error(f"Error connecting to Ollama: {e}")
        logger.error("Please make sure Ollama is running and accessible")
        return False

def process_category(category, source_dirs):
    """Process a single knowledge base category"""
    try:
        logger.info(f"Processing {category}...")
        
        # Create vectorstore directory if it doesn't exist
        kb_dir = VECTORSTORE_DIR / category
        kb_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if any documents exist in the source directories
        doc_count = 0
        markdown_files = set()  # Use set to handle duplicates
        for source_dir in source_dirs:
            logger.info(f"Checking directory: {source_dir}")
            if source_dir.exists():
                files = set(source_dir.glob("**/*.md"))  # Convert to set
                doc_count += len(files)
                markdown_files.update(files)
                logger.info(f"Found {len(files)} unique markdown files in {source_dir}:")
                for f in files:
                    logger.info(f"  - {f}")
                    # Verify file is readable
                    try:
                        with open(f, 'r') as test_file:
                            content = test_file.read()
                            # Remove duplicate lines
                            unique_lines = []
                            seen_lines = set()
                            for line in content.splitlines():
                                if line not in seen_lines:
                                    unique_lines.append(line)
                                    seen_lines.add(line)
                            content = '\n'.join(unique_lines)
                            logger.info(f"  ✓ File is readable: {f} (size: {len(content)} bytes)")
                    except Exception as e:
                        logger.error(f"  ✗ File is not readable: {f} - {str(e)}")
                        continue
            else:
                logger.warning(f"Directory does not exist: {source_dir}")
        
        if doc_count == 0:
            logger.warning(f"No markdown documents found for {category}")
            return False

        # Initialize embeddings
        logger.info("Initializing Ollama embeddings...")
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # Load documents
        logger.info("Loading documents...")
        all_docs = []
        for file_path in markdown_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Remove duplicate lines
                    unique_lines = []
                    seen_lines = set()
                    for line in content.splitlines():
                        if line not in seen_lines:
                            unique_lines.append(line)
                            seen_lines.add(line)
                    content = '\n'.join(unique_lines)
                    all_docs.append({"content": content, "source": str(file_path)})
                logger.info(f"Successfully loaded: {file_path}")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")
                continue
        
        if not all_docs:
            logger.warning(f"No documents loaded for {category}")
            return False
        
        # Split documents into chunks
        logger.info("Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.create_documents([doc["content"] for doc in all_docs])
        logger.info(f"Split into {len(chunks)} chunks")
        
        # Create FAISS index
        logger.info("Creating FAISS index...")
        db = FAISS.from_documents(chunks, embeddings)
        
        # Save the index
        logger.info(f"Saving FAISS index to {kb_dir}...")
        db.save_local(str(kb_dir))
        logger.info(f"Successfully saved FAISS index for {category}")
        
        return True
            
    except Exception as e:
        logger.error(f"Error processing {category}: {str(e)}")
        logger.error("Traceback:", exc_info=True)
        return False

def main():
    """Main function to build all knowledge bases"""
    logger.info("Starting RAG Builder for Barry Sharp Pro Mover")
    
    # Check if Ollama is running
    if not check_ollama_running():
        return
    
    # Create vectorstore directory if it doesn't exist
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Process each category
    results = {}
    for category, source_dirs in KB_CATEGORIES.items():
        start_time = time.time()
        success = process_category(category, source_dirs)
        elapsed_time = time.time() - start_time
        results[category] = {
            "success": success,
            "time": f"{elapsed_time:.2f} seconds"
        }
    
    # Print summary
    logger.info("\nRAG Builder Summary:")
    for category, result in results.items():
        status = "✅ Success" if result["success"] else "❌ Failed"
        logger.info(f"{category}: {status} ({result['time']})")
    
    # Save metadata
    metadata = {
        "build_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "categories": results
    }
    with open(VECTORSTORE_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"\nRAG Builder completed. Metadata saved to {VECTORSTORE_DIR / 'metadata.json'}")

if __name__ == "__main__":
    main()