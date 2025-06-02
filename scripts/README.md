# Barry Sharp Pro Mover - Scripts

This directory contains utility scripts for the Barry Sharp Pro Mover project.

## RAG System Scripts

The following scripts implement Phase 1 of the development plan, which involves setting up the Retrieval-Augmented Generation (RAG) system:

### build_rag.py

This script builds the RAG system by processing documents from the `docs` directory and creating FAISS indexes in the `vectorstore` directory.

**Features:**
- Loads documents from the `docs` directory
- Splits them into chunks
- Creates embeddings using Ollama's `nomic-embed-text` model
- Stores the embeddings in FAISS indexes in the `vectorstore` directory

**Usage:**
```bash
# Make sure Ollama is running
python3 scripts/build_rag.py
```

**Requirements:**
- Ollama installed and running
- `nomic-embed-text` model available in Ollama (will be pulled automatically if not present)
- Python packages: langchain, langchain_community, faiss-cpu

### test_rag.py

This script tests the RAG system by allowing you to ask questions about the game design document.

**Features:**
- Loads the FAISS indexes from the `vectorstore` directory
- Creates a simple RAG chain using Ollama's `mistral` model
- Provides an interactive Q&A interface

**Usage:**
```bash
# Test the design knowledge base (default)
python3 scripts/test_rag.py

# Test a specific knowledge base
python3 scripts/test_rag.py --kb art_kb
```

**Available Knowledge Bases:**
- `design_kb` - Game design documents
- `art_kb` - Art-related documents
- `code_kb` - Code-related documents
- `dialogue_kb` - Dialogue and narrative documents
- `music_kb` - Music and sound documents
- `shared_kb` - Shared documents
- `qa_kb` - All documents (for QA purposes)

**Requirements:**
- Ollama installed and running
- `nomic-embed-text` and `mistral:7b-instruct-q4_K_M` models available in Ollama (will be pulled automatically if not present)
- Python packages: langchain, langchain_community, faiss-cpu

## Installation

To install the required Python packages:

```bash
pip install langchain langchain_community faiss-cpu
```

Make sure Ollama is installed and running. You can install Ollama from [https://ollama.ai/](https://ollama.ai/).