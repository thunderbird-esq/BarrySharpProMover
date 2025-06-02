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

### LangFlow Integration
```bash
# Start LangFlow server
./start_langflow.sh

# Bootstrap project management
./bootstrap_pm_backbone.sh
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
- Python 3.x (for validation scripts)
- LangFlow (for automation workflows)

## Contributing

Refer to the documentation in `docs/` for development guidelines and project specifications.