# Scripts for Barry Sharp Pro Mover

This directory contains various utility and automation scripts for the Barry Sharp Pro Mover project.

## Table of Contents

- [RAG System Scripts](#rag-system-scripts)
  - [build_rag.py](#build_ragpy)
  - [test_rag.py](#test_ragpy)
- [Utility Scripts](#utility-scripts)
  - [bootstrap_pm_backbone.sh](#bootstrap_pm_backbonesh)
  - [build/test_run_all.sh](#buildtest_run_allsh)
  - [build/test_validation.sh](#buildtest_validationsh)
  - [sync_gbsres.sh](#sync_gbsressh)
  - [snapshot.sh](#snapshotsh)
- [Other Scripts](#other-scripts)
- [Installation Notes](#installation-notes)

## RAG System Scripts

These scripts are related to the Retrieval-Augmented Generation (RAG) system, primarily for managing the project's knowledge base.

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

## Utility Scripts

This section describes general-purpose utility scripts for development, build, and version control tasks.

### bootstrap_pm_backbone.sh
*   **Purpose**: Initializes or resets the project management directory structure and placeholder files. This script is typically used once during initial project setup or if the project management artifacts in the `memory/` and `staging/` directories need to be recreated from a clean state.
*   **Typical Use**: Run during initial project setup.
    ```bash
    ./bootstrap_pm_backbone.sh
    ```

### build/test_run_all.sh
*   **Purpose**: Performs a comprehensive local build and validation sequence. This typically includes running all asset validations, compiling the ROM, and potentially other checks. It's a way to manually ensure the project is in a good state.
*   **When to Use**: Before committing significant changes, or when you want to perform a full local sanity check of the project.
    ```bash
    ./scripts/build/test_run_all.sh
    ```

### build/test_validation.sh
*   **Purpose**: Executes all available validation scripts (e.g., for background tiles, scene limits, JSON files). This script focuses solely on validation without performing a full build.
*   **When to Use**: When you want to quickly check if assets and project files meet the defined criteria, especially after making changes to assets.
    ```bash
    ./scripts/build/test_validation.sh
    ```

### sync_gbsres.sh
*   **Purpose**: Synchronizes and maintains the integrity of GB Studio's `.gbsres` asset metadata files. GB Studio uses these files to track assets, and they can sometimes become out of sync or contain outdated information. This script helps clean them up.
*   **Importance**: Crucial for preventing asset-related issues in GB Studio.
*   **When to Use**: Run this script if you encounter unexpected asset behavior in GB Studio, after manually adding, removing, or renaming asset files, or as a routine maintenance step.
    ```bash
    ./scripts/sync_gbsres.sh
    ```

### snapshot.sh
*   **Purpose**: Creates a quick Git snapshot by adding all changes, committing them with a timestamped message, and pushing to the remote repository. This is useful for quickly saving your current work-in-progress.
*   **Typical Use**: When you want to save your current state without crafting a detailed commit message, often used during intensive development sessions.
    ```bash
    ./scripts/snapshot.sh "Optional short message for context"
    ```

## Other Scripts

This directory may contain other scripts not listed above, such as:
- `automation_control.sh`: Manages the LangFlow automation system (see `docs/AUTOMATION_GUIDE.md`).
- `notify_cli.sh`: A simple command-line notification script.

Refer to individual script comments or specific documentation for their usage.

## Installation Notes
For Python scripts, ensure you have the necessary dependencies installed, typically within your project's virtual environment (`venv/`). The `automation_control.sh` script, for instance, expects LangFlow and its dependencies to be installed via `pip install -e .` in the project root.
Specific requirements for RAG scripts are listed under their section.