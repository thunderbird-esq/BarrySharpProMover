# Barry Sharp Pro Mover - GB Studio Game Project

A Game Boy game developed using GB Studio with integrated LangFlow automation and build tools.

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
- `langflow_components/` - Custom LangFlow components for automation
- `langflow_projects/` - LangFlow workflow definitions

### Documentation
- `docs/` - Project documentation organized by category
  - `design/` - Game design documents
  - `shared/` - General project documentation
  - `art/`, `code/`, `dialogue/`, `music/` - Category-specific docs

### Project Management
- `memory/` - Project state and approval tracking
- `feedback/` - User feedback and testing results
- `staging/` - Temporary staging area for outputs
- `vectorstore/` - Knowledge base storage

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

## Requirements

- GB Studio (with CLI tools)
- Node.js (for GB Studio CLI)
- Python 3.9+ and pip (for validation scripts and LangFlow setup)

## LangFlow Setup and Custom Components

This project uses LangFlow for automation workflows, with custom components tailored for game development tasks.

**Requirements:**

*   Python 3.9+ and pip
*   [GB Studio](https://www.gbstudio.dev/) (for game development itself)

**Setup Instructions:**

1.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows: venv\Scriptsctivate
    ```

2.  **Install dependencies (including LangFlow):**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Make custom components available to LangFlow:**
    The custom components for this project are located in `.langflow/components/`. To make them accessible to LangFlow, run the following script:
    ```bash
    python .langflow/components/import_nodes.py
    ```
    This script copies the component files to the `~/.langflow/components/` directory, where LangFlow can discover them.

4.  **Run LangFlow:**
    ```bash
    langflow run
    ```
    You can then access the LangFlow UI, usually at `http://127.0.0.1:7860`.

5.  **Import Flows:**
    The project's LangFlow flows are stored in `.langflow/flows/`. You can import these JSON files into the LangFlow UI.

## Contributing

Refer to the documentation in `docs/` for development guidelines and project specifications.