# n8n Workflow Guide

This document provides an overview of the n8n workflows used in this project for automation, task management, and AI-assisted development.

## Core Workflows

### 1. TheConductor_PM_n8n
*   **Purpose:** Acts as the central project manager, parsing user commands and routing tasks.
*   **Triggers:** [e.g., Manual, Webhook]
*   **Key Functions:** [e.g., LLM-based task parsing, state management, RAG integration]
*   **Configuration:** [Any specific setup notes]

### 2. Build_Workflow_n8n
*   **Purpose:** Handles the game ROM and web build processes.
*   **Triggers:** [e.g., Manual, Webhook]
*   **Key Steps:** [e.g., Git pull, resource syncing, GB Studio CLI execution, notifications]

### 3. Enhanced_Automation_n8n
*   **Purpose:** Provides CI/CD-like automation including file watching, automated builds, and reporting.
*   **Triggers:** [e.g., File System Events, Webhooks, Scheduled (Cron)]
*   **Key Functions:** [e.g., CI/CD pipeline execution, report generation, ledger logging]

### 4. RAG_Index_Builder_n8n
*   **Purpose:** Builds and maintains the FAISS vector store for the RAG pipeline.
*   **Triggers:** [e.g., Manual, Scheduled]
*   **Key Steps:** [e.g., Document loading, text splitting, embedding generation, FAISS index updates]

### 5. RAG_Retriever_n8n
*   **Purpose:** Retrieves relevant information from the RAG store and uses an LLM to answer queries.
*   **Triggers:** [e.g., Called by other workflows, Webhook]
*   **Key Steps:** [e.g., Query embedding, FAISS search, context formatting, LLM Q&A]

## Helper Scripts (`tools/`)
*   Briefly describe the purpose of key scripts in `tools/` (e.g., `ci_cd_pipeline.py`, `manage_faiss.py`, `gbstudio_build.py`) and how they are invoked by n8n workflows (typically via Execute Command nodes).

## State Management (`memory/`)
*   Explain the role of `approval_queue.json`, `pm_ledger.jsonl`, and `project_mem.json` and how n8n workflows interact with them (typically via Function nodes using `fs` or Execute Command nodes).

## Customizing Workflows
*   [General tips on how to modify or extend the workflows in n8n]
