#!/usr/bin/env python3
"""
RAG Tester Script for Barry Sharp Pro Mover
Implements Phase 1 validation of the LANGFLOW-DEV-PLAN.md

This script:
1. Loads the FAISS indexes from the vectorstore directory
2. Creates a simple RAG chain using Ollama's mistral model
3. Allows the user to ask questions about the game design document
"""

import os
import sys
import json
from pathlib import Path
import logging
import argparse

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
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain_community.llms import Ollama
    import ollama
except ImportError as e:
    logger.error(f"Required package not found: {e}")
    logger.error("Please install required packages: pip install langchain langchain_community faiss-cpu")
    sys.exit(1)

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

def check_ollama_running():
    """Check if Ollama is running and the required models are available"""
    try:
        # Check if Ollama is running
        models = ollama.list()
        
        # Check if required models are available
        model_names = [model.get('name') for model in models.get('models', [])]
        required_models = ['nomic-embed-text', 'mistral:7b-instruct-q4_K_M']
        
        for model in required_models:
            if model not in model_names and not any(model in name for name in model_names):
                logger.warning(f"{model} model not found in Ollama")
                logger.info(f"Pulling {model} model...")
                ollama.pull(model)
                logger.info("Model pulled successfully")
        return True
    except Exception as e:
        logger.error(f"Error connecting to Ollama: {e}")
        logger.error("Please make sure Ollama is running and accessible")
        return False

def load_vectorstore(kb_name):
    """Load a vectorstore from the given knowledge base name"""
    kb_dir = VECTORSTORE_DIR / kb_name
    
    if not kb_dir.exists():
        logger.error(f"Knowledge base {kb_name} not found in {VECTORSTORE_DIR}")
        return None
    
    try:
        # Initialize embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # Load FAISS index
        vectorstore = FAISS.load_local(str(kb_dir), embeddings)
        logger.info(f"Loaded FAISS index from {kb_dir}")
        
        return vectorstore
    except Exception as e:
        logger.error(f"Error loading vectorstore {kb_name}: {e}")
        return None

def create_qa_chain(vectorstore):
    """Create a QA chain using the given vectorstore"""
    try:
        # Create prompt template
        template = """
        You are an AI assistant for the game development project "Barry Sharp's Pro Mover".
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Keep your answers concise and directly related to the context provided.
        
        Context: {context}
        
        Question: {question}
        
        Answer:
        """
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        
        # Initialize LLM
        llm = Ollama(model="mistral:7b-instruct-q4_K_M", temperature=0.2)
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt}
        )
        
        return qa_chain
    except Exception as e:
        logger.error(f"Error creating QA chain: {e}")
        return None

def interactive_qa(qa_chain):
    """Run an interactive QA session"""
    print("\n=== Barry Sharp Pro Mover RAG Tester ===\n")
    print("Ask questions about the game design document or type 'exit' to quit.\n")
    
    while True:
        question = input("\nQuestion: ")
        if question.lower() in ["exit", "quit", "q"]:
            break
        
        try:
            result = qa_chain({"query": question})
            print("\nAnswer:")
            print(result["result"])
        except Exception as e:
            logger.error(f"Error processing question: {e}")

def main():
    """Main function to test the RAG system"""
    parser = argparse.ArgumentParser(description="Test the RAG system for Barry Sharp Pro Mover")
    parser.add_argument(
        "--kb", 
        default="design_kb", 
        choices=["design_kb", "art_kb", "code_kb", "dialogue_kb", "music_kb", "shared_kb", "qa_kb"],
        help="Knowledge base to query (default: design_kb)"
    )
    args = parser.parse_args()
    
    logger.info(f"Starting RAG Tester for Barry Sharp Pro Mover using {args.kb}")
    
    # Check if Ollama is running
    if not check_ollama_running():
        return
    
    # Load vectorstore
    vectorstore = load_vectorstore(args.kb)
    if not vectorstore:
        return
    
    # Create QA chain
    qa_chain = create_qa_chain(vectorstore)
    if not qa_chain:
        return
    
    # Run interactive QA
    interactive_qa(qa_chain)
    
    logger.info("RAG Tester completed")

if __name__ == "__main__":
    main()