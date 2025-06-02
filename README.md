# Barry Sharp Pro Mover - GB Studio Game Project

A Game Boy game developed using GB Studio with integrated n8n automation and build tools.

## Project Structure

### Core Game Files
- `BARRY-SHARP-PRO-MOVER-1.gbsproj` - Main GB Studio project file
- `assets/` - All game assets (sprites, backgrounds, music, sounds, etc.)
- `build/` - Compiled game outputs (ROM and web builds)

### Development Tools
- `Makefile` - Build automation using GB Studio CLI
- `scripts/` - Development and validation scripts
  - `build/` - Build-related scripts
  - `validation/` - Asset validation tools
- `tools/` - Utility scripts for automation and project management.
- `n8n_workflows/` - n8n workflow definitions.

### Documentation
- `docs/` - Project documentation organized by category
  - `design/` - Game design documents
  - `shared/` - General project documentation
  - `art/`, `code/`, `dialogue/`, `music/` - Category-specific docs

### Project Management
- `memory/` - Project state and approval tracking
- `feedback/` - User feedback and testing results
- `staging/` - Temporary staging area for outputs
- `vectorstore/` - Knowledge base storage for RAG.

## Quick Start

### Building the Game
```bash
# Build ROM file
make build-rom

# Build web version
make build-web

# Clean build artifacts
make clean
```

### Development Scripts
```bash
# Validate assets
./scripts/validation/check_bg_tiles.py
./scripts/validation/check_scene_limits.py

# Sync GB Studio resources
./scripts/sync_gbsres.sh

# Create project snapshot
./scripts/snapshot.sh
```

## Project Automation with n8n

This project utilizes n8n for various automation tasks, including CI/CD, build management, task processing, and AI-assisted development.

### Prerequisites
List n8n version, Node.js, Python, Ollama, gb-studio-cli, etc.

### Setup
Explain how to import workflows from `n8n_workflows/` into n8n. Detail environment variable setup for API keys like Google Gemini, Ollama URL if not default.

### Running Key Workflows
Instructions for `TheConductor_PM_n8n`, `Build_Workflow_n8n`, `Enhanced_Automation_n8n`.

### Architecture Overview
Briefly describe the n8n-based architecture, including key workflows and how they use scripts from `tools/` and state from `memory/`.

## Asset Organization

All game assets are consolidated in the `assets/` directory:
- `backgrounds/` - Background images
- `sprites/` - Character and object sprites
- `music/` - Background music files
- `sounds/` - Sound effects
- `fonts/` - Custom fonts
- `palettes/` - Color palettes
- `tilesets/` - Tile graphics
- `ui/` - User interface elements

## Build System

The project uses a Makefile that leverages the GB Studio CLI for consistent builds:
- Automated ROM compilation
- Web build generation
- Asset validation
- Clean build management
Some of these Makefile targets may also be invoked via n8n workflows.

## Requirements

- GB Studio (with CLI tools)
- Node.js (for GB Studio CLI and n8n)
- Python 3.x (for utility and automation scripts)
- n8n (for workflow automation)
- Ollama (for local LLM operations, if used)

## Contributing

Refer to the documentation in `docs/` (including `docs/N8N_WORKFLOW_GUIDE.md`) for development guidelines and project specifications.