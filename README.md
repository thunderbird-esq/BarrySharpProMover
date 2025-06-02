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

This section provides a brief overview of how to get the project set up and running. For more detailed instructions, especially regarding the automation system, please refer to `docs/AUTOMATION_GUIDE.md`.

**1. Environment Setup:**

Before you can build the game or run automation workflows, you need to set up your development environment:

*   **Install Core Dependencies:** Ensure you have Git, Node.js, and the `make` utility installed on your system.
*   **Python Virtual Environment:** This project uses a Python virtual environment to manage dependencies like LangFlow.
    *   Navigate to the project root directory.
    *   Create the virtual environment: `python3 -m venv venv`
    *   Activate it: `source venv/bin/activate` (on macOS/Linux) or `source venv/Scripts/activate` (on Windows with Git Bash/WSL).
    *   Install project dependencies (including LangFlow and custom components): `pip install -e .`
    *   For detailed setup, see the "Environment Setup" section in `docs/AUTOMATION_GUIDE.md`. The `scripts/automation_control.sh` script also expects this setup.

**2. Common Operations:**

Once your environment is set up and the virtual environment is active:

**Building the Game:**
The `Makefile` provides targets for building the game:
```bash
# Build the game ROM (outputs to build/rom.gb)
make build-rom

# Build the web version (outputs to build/web/)
make build-web

# Clean build artifacts
make clean
```
*Note: Building requires GB Studio CLI. Refer to "GB Studio CLI Dependency Management" below if it's not in your PATH.*

**Running Validation Scripts:**
Individual validation scripts can be run directly (ensure your venv is active if they are Python scripts):
```bash
# Example: Validate background tiles
python3 scripts/validation/check_bg_tiles.py assets/backgrounds/*.png

# Example: Validate scene limits
python3 scripts/validation/check_scene_limits.py project/scenes/
```
*Many validations are also available via `make` targets (e.g., `make check-bg`).*

**Interacting with the Automation System:**
The primary script for managing the LangFlow-based automation system is `scripts/automation_control.sh`. Ensure your virtual environment is active.
```bash
# Start the automation system (LangFlow server + file watcher)
./scripts/automation_control.sh start

# Check the status of the automation system
./scripts/automation_control.sh status

# Stop the automation system
./scripts/automation_control.sh stop
```
*Refer to `docs/AUTOMATION_GUIDE.md` for full details on the automation system's capabilities and configuration (including `LANGFLOW_HOST` and `LANGFLOW_PORT` environment variables).*

**Other Utility Scripts:**
```bash
# Example: Sync GB Studio resources (if applicable to your workflow)
# ./scripts/sync_gbsres.sh

# Example: Create a project snapshot (if applicable)
# ./scripts/snapshot.sh
```
*(Review script contents and `docs/` for relevance to current project state).*

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

### Configuring the GB Studio CLI Path
By default, the build system assumes that `gb-studio-cli` (or `gb-studio-cli.js`) is available in your system's PATH.
If the GB Studio CLI is installed in a custom location, you can specify the path to the executable (e.g., `/path/to/gb-studio/out/cli/gb-studio-cli.js` or `C:\path\to\gb-studio-cli.js`) by setting the `GBSTUDIO_CLI_PATH` environment variable.

For example:
```bash
export GBSTUDIO_CLI_PATH="/path/to/your/gb-studio/out/cli/gb-studio-cli.js"
make build-rom
```
This variable is respected by both the `Makefile` and the LangFlow components.

## GB Studio CLI Dependency Management

It is strongly recommended to install `gb-studio-cli` globally and ensure it is available in your system's `PATH`. This is the most straightforward way to ensure the build tools work out-of-the-box, as the default configuration assumes `gb-studio-cli` is accessible via the `PATH`.

If you are unsure how to install it, please refer to the official GB Studio documentation. Typically, if it's distributed via npm, you would install it using a command like:
```bash
npm install -g gb-studio-cli
```
*(Please verify the actual command from the official GB Studio resources.)*

For specific project needs, or if you prefer not to install the CLI globally (e.g., to use a particular version for this project only), you can:
1. Download or place the `gb-studio-cli.js` file (and any associated files it requires, often found in a `cli` or `out/cli` directory within the GB Studio installation/repository) into a known location within your project or elsewhere on your system.
2. Set the `GBSTUDIO_CLI_PATH` environment variable to point directly to this `gb-studio-cli.js` file. For example:
   ```bash
   export GBSTUDIO_CLI_PATH="./tools/gb-studio/out/cli/gb-studio-cli.js"
   make build-rom
   ```
   Or on Windows:
   ```powershell
   $env:GBSTUDIO_CLI_PATH = "C:\path\to\your\gb-studio\out\cli\gb-studio-cli.js"
   make build-rom
   ```

## Requirements

The following are essential for working with this project:

- **Git**: For version control.
- **Python 3.x**: Required for scripting and running LangFlow.
    - **Python Virtual Environment (`venv/`)**: Crucial for isolating project dependencies. Setup involves creating the venv, activating it, and running `pip install -e .` to install components and their dependencies (like LangFlow) as defined in `pyproject.toml`. The `scripts/automation_control.sh` script expects this venv at `PROJECT_ROOT/venv/` and attempts to activate it. Detailed instructions are in `docs/AUTOMATION_GUIDE.md`.
- **Node.js**: Necessary for running the GB Studio CLI (which is a Node.js application). The `scripts/automation_control.sh` script checks for `node` in your PATH.
- **`make`**: The Make utility is used to run tasks defined in the `Makefile` (e.g., `make build-rom`). The `scripts/automation_control.sh` script checks for `make` in your PATH.
- **GB Studio**: The core game development application.
    - **GB Studio CLI**: The command-line interface for GB Studio. This is used by the `Makefile` for building the game. It's recommended to have it installed globally and in your system `PATH`. Alternatively, you can set the `GBSTUDIO_CLI_PATH` environment variable (default is `gb-studio-cli` if not set). See the "GB Studio CLI Dependency Management" section for more details.
- **LangFlow**: The framework used for visual workflow automation. This is installed into the project's Python virtual environment when you run `pip install -e .`. The `scripts/automation_control.sh` script manages starting and stopping the LangFlow server. Its host and port can be configured via `LANGFLOW_HOST` (default: `127.0.0.1`) and `LANGFLOW_PORT` (default: `7860`) environment variables.

## Contributing

Refer to the documentation in `docs/` for development guidelines and project specifications.