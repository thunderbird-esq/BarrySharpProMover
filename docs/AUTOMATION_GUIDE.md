# Barry Sharp Pro Mover - Enhanced Automation Guide

This guide covers the enhanced automation system that provides continuous integration, deployment, and file monitoring capabilities for the Barry Sharp Pro Mover project.

## Environment Setup

Before using the automation system, it's crucial to set up a dedicated Python virtual environment for this project. This ensures that all Python-based tools, including LangFlow and the custom project components, run with consistent dependencies.

The main control script, `scripts/automation_control.sh`, is designed to automatically detect and activate this virtual environment if it's located at `$PROJECT_ROOT/venv/`.

**1. Create the Virtual Environment:**
Navigate to the project root directory (`barry-sharp-pro-mover`) in your terminal and run:
```bash
python3 -m venv venv
```
This will create a `venv` directory within your project.

**2. Activate the Virtual Environment:**
On macOS and Linux:
```bash
source venv/bin/activate
```
On Windows (Git Bash or WSL):
```bash
source venv/Scripts/activate
```
Your terminal prompt should change to indicate that the virtual environment is active (e.g., `(venv) your-prompt$`).

**3. Install Dependencies:**
With the virtual environment activated, install the project's components and their dependencies (including LangFlow). The `pyproject.toml` file defines these.
```bash
pip install -e .
```
The `-e .` flag installs the project in "editable" mode, which is useful for development as changes to your local component code are reflected immediately. This command should install `langflow` as it's listed as a dependency in `pyproject.toml`, along with other necessary packages.

**Verification:**
After installation, you can verify that `langflow` is installed in your venv:
```bash
which langflow
# Should point to .../barry-sharp-pro-mover/venv/bin/langflow
langflow --version
```

**Note on the `langflow/` subdirectory:** This note is being expanded and moved to its own subsection below.

Once the environment is set up and activated, you can use `scripts/automation_control.sh` to manage the automation system. If you open a new terminal, remember to reactivate the virtual environment (`source venv/bin/activate`). The `automation_control.sh` script itself will also attempt to activate the `venv/` directory if it finds it, and will check for essential external tools like `make` and `node`.

### Understanding the `langflow/` Subdirectory

The project repository includes a subdirectory named `langflow/`. It's important to understand its purpose to avoid confusion:

*   **Full LangFlow Source Code:** This directory contains a complete source code distribution of the LangFlow application itself.
*   **Not for Project Automation:** The project's automation system (managed by `scripts/automation_control.sh`) **does not** run LangFlow directly from this `langflow/` subdirectory. Instead, it relies on LangFlow being installed as a Python package within the project's dedicated virtual environment (`venv/`), typically via the `pip install -e .` command which installs dependencies listed in `pyproject.toml`.
*   **Purpose of the Embedded Source:** The `langflow/` subdirectory is primarily included for:
    *   **Reference:** Developers can easily browse or search the LangFlow source code.
    *   **LangFlow Development:** If you intend to contribute to or debug LangFlow itself, this embedded source provides a convenient way to do so in the context of this project.
*   **Focus for Project Game Automation:** For tasks related to developing, running, or managing *this project's game automation workflows*, you should focus on:
    *   The Python virtual environment (`venv/`) and the version of LangFlow installed within it.
    *   The project's custom LangFlow components, primarily located in `.langflow/components/` (for local development and registration) and packaged within `langflow_components/` (as defined in `pyproject.toml`).
*   **Distinct Custom Components:** Note that the embedded `langflow/` directory might also contain its own `custom_components` folder (e.g., `langflow/custom_components/`). This is part of the LangFlow application's own structure and should not be confused with this project's primary component directories mentioned above. The components relevant to this game project are those managed by our `pyproject.toml` and typically found in `.langflow/components/` or `langflow_components/`.

### A Note on Custom Python Component Sources

Understanding where custom Python components for LangFlow are managed in this project is important:

*   **Primary Active Location (`.langflow/components/`):** When you are actively developing or modifying custom LangFlow components (the Python classes that define new nodes), the primary directory LangFlow typically interacts with for loading and saving these components via its UI or import mechanisms is `.langflow/components/`. Changes made here are what you'll see reflected when running LangFlow via `scripts/automation_control.sh`.
*   **Packaged Source (`langflow_components/` and `pyproject.toml`):**
    *   The `pyproject.toml` file at the root of this project defines a Python package named `barrysharp-components`.
    *   This package lists `langflow_components/` as its source code directory (i.e., `packages = ["langflow_components"]` in `pyproject.toml`).
    *   Crucially, `pyproject.toml` also specifies `langflow>=1.4` as a dependency.
*   **Installation via `pip install -e .`:** When you run `pip install -e .` (editable install) in the project root (with your `venv/` activated):
    *   It installs LangFlow itself (and its dependencies) into your virtual environment because it's listed in `pyproject.toml`.
    *   It also makes the `barrysharp-components` package (with code from `langflow_components/`) available in the environment. LangFlow can then discover entry points defined in this package (like `gbstudio-build = "langflow_components.tools.gbstudio_build:GBStudioBuild"` as specified in `pyproject.toml` under `[project.entry-points."langflow_components"]`).
*   **Current Development Workflow & Future Considerations:**
    *   Currently, the `.langflow/components/` directory serves as the "hot" or active development area for components used directly by the running LangFlow instance.
    *   The `langflow_components/` directory and its packaging via `pyproject.toml` ensure that LangFlow and other core Python dependencies are correctly installed. It also provides a mechanism for formally packaging and distributing these components if needed in the future, or for LangFlow to discover them via entry points.
    *   If you are developing a new component or significantly modifying an existing one, you would typically work within `.langflow/components/`. To formally package or share it, or ensure it's discoverable via entry points, you might then also place its source into the `langflow_components/` directory and update `pyproject.toml` if necessary.
    *   This distinction is important to prevent confusion. For now, **active development and modification of component Python files for immediate use in LangFlow should primarily occur in `.langflow/components/`**. The `langflow_components/` directory serves more as a formal packaging source and for dependency management of LangFlow itself. This setup might evolve as component management practices for the project are refined.

## Overview

The enhanced automation system includes:

- **CI/CD Pipeline**: Automated build, test, and deployment
- **File Watcher**: Real-time monitoring of project files
- **LangFlow Integration**: Visual workflow management
- **Notification System**: Alerts for build status and changes
- **Status Reporting**: Comprehensive project health reports

## Quick Start

This section assumes you have completed the "Environment Setup" steps above, including creating and activating the virtual environment and installing dependencies with `pip install -e .`.

### 1. Start the Automation System

```bash
# Using the control script
./scripts/automation_control.sh start

# Or using Make
make automation-start

# Or start development environment
make dev-start
```

### 2. GB Studio CLI Dependency Management

A crucial part of the automation, especially for building the game, is the GB Studio Command Line Interface (CLI).

**Recommendation: Global Installation**

It is strongly recommended to install `gb-studio-cli` globally and ensure it is available in your system's `PATH`. This aligns with the default configuration of the build tools (`Makefile` and LangFlow components) which assume `gb-studio-cli` is accessible directly.

If you are unsure how to install it, please refer to the official GB Studio documentation. If it's an npm package, the command would typically be:
```bash
npm install -g gb-studio-cli
```
*(Always verify the installation command from official GB Studio resources.)*

**Alternative: Local/Specific Version**

If you need to use a specific version of the CLI for this project, or prefer not to install it globally:
1.  Download or place the `gb-studio-cli.js` file (and its necessary dependencies, often found in a `cli` or `out/cli` folder within the main GB Studio software directory) into a known location. This could be within a `tools/` directory in this project, for example.
2.  Set the `GBSTUDIO_CLI_PATH` environment variable to the full path of this `gb-studio-cli.js` file.
    *   On Linux/macOS:
        ```bash
        export GBSTUDIO_CLI_PATH="/path/to/your/gb-studio-cli.js"
        ```
    *   On Windows (PowerShell):
        ```powershell
        $env:GBSTUDIO_CLI_PATH = "C:\path\to\your\gb-studio-cli.js"
        ```
    The build scripts and LangFlow components will use this path. The default value if this variable is not set is `gb-studio-cli`, assuming it's in your system's PATH.

### 3. Access the LangFlow UI

The LangFlow UI will be available at the address configured by `LANGFLOW_HOST` and `LANGFLOW_PORT` environment variables (defaults to http://127.0.0.1:7860).
Open your browser to this address after starting the automation system.

### 4. Monitor Status

```bash
# Check system status
./scripts/automation_control.sh status

# View logs
./scripts/automation_control.sh logs

# Generate report
./scripts/automation_control.sh report
```

## Components

### CI/CD Pipeline (`ci_cd_pipeline.py`)

Automated pipeline that:
- Runs validation checks
- Builds the ROM
- Executes tests
- Deploys to staging
- Sends notifications

**Usage:**
```bash
# Manual trigger
./scripts/automation_control.sh pipeline

# Or via Make
make automation-pipeline
```

### Enhanced File Watcher (`enhanced_file_watcher.py`)

Monitors project files and automatically triggers builds when changes are detected.

**Monitored Directories:**
- `assets/sprites/`
- `assets/backgrounds/`
- `assets/music/`
- `assets/sounds/`
- `scripts/`
- `docs/`
- `BARRY-SHARP-PRO-MOVER-1.gbsproj`

**Features:**
- Debounced change detection (5-second default)
- Automatic CI/CD triggering
- Approval queue integration
- Comprehensive logging

### GB Studio Build Component (`gbstudio_build.py`)

Direct integration with GB Studio CLI for ROM compilation. This component relies on `gb-studio-cli` being available, either in the system `PATH` or via the `GBSTUDIO_CLI_PATH` environment variable as described in the "GB Studio CLI Dependency Management" section.

**Features:**
- ROM and web builds
- OpenEmu integration
- Error handling and reporting

### Notification System (`notifier.py`)

Centralized notification system for automation events.

**Supported Methods:**
- CLI notifications (default)
- Extensible for email, webhooks, etc.

### Report Generator (`report_gen.py`)

Generates comprehensive status reports including:
- Pending approvals
- Recent activity
- Build history
- System metrics

## Automation Control Script

The `scripts/automation_control.sh` script is the primary tool for managing the automation system.
Key features of the script:
- Automatically attempts to activate the Python virtual environment from `$PROJECT_ROOT/venv/`.
- Checks for essential system dependencies like `make` and `Node.js` before starting.
- Uses environment variables for configuration (e.g., `LANGFLOW_HOST`, `LANGFLOW_PORT`).
- Manages the LangFlow server and the file watcher process.

### Commands

```bash
# System control
./scripts/automation_control.sh start     # Start automation
./scripts/automation_control.sh stop      # Stop automation
./scripts/automation_control.sh restart   # Restart automation
./scripts/automation_control.sh status    # Show status

# Operations
./scripts/automation_control.sh pipeline  # Trigger CI/CD
./scripts/automation_control.sh report    # Generate report
./scripts/automation_control.sh logs      # Show logs
./scripts/automation_control.sh help      # Show help
```

## Make Targets

The enhanced Makefile (`Makefile.automation`) provides additional targets:

### Automation Management
```bash
make automation-start      # Start automation system
make automation-stop       # Stop automation system
make automation-restart    # Restart automation system
make automation-status     # Check status
make automation-install    # Install components
make automation-test       # Test components
make automation-clean      # Clean artifacts
```

### Development Workflow
```bash
make dev-start            # Start development environment
make dev-stop             # Stop development environment
make dev-build            # Quick development build
make dev-watch            # Watch for changes
```

### Enhanced Build Targets
```bash
make build-with-automation  # Build with full pipeline
make deploy-staging        # Deploy to staging
make full-pipeline         # Complete CI/CD pipeline
make release              # Create production release
```

## LangFlow Integration

### Enhanced Automation Flow

The `enhanced_automation_flow.json` provides a comprehensive workflow with:

- **Command Parser**: Interprets user commands
- **File Watcher**: Monitors project changes
- **CI/CD Pipeline**: Automated build and test
- **Approval Queue**: Manages pending tasks
- **Notification Hub**: Centralized alerts
- **Report Generator**: Status reporting

### Available Commands

In the LangFlow UI, you can use these commands:
- `start-watch`: Start file monitoring
- `run-pipeline`: Execute CI/CD pipeline
- `stop-watch`: Stop file monitoring
- `status`: Get system status
- `build-only`: Build ROM without testing
- `full-pipeline`: Run complete CI/CD

## File Structure

```
barry-sharp-pro-mover/
├── langflow_components/          # Custom LangFlow components
│   ├── ci_cd_pipeline.py        # CI/CD automation
│   ├── enhanced_file_watcher.py # File monitoring
│   ├── gbstudio_build.py        # GB Studio integration
│   ├── notifier.py              # Notification system
│   └── report_gen.py            # Report generation
├── langflow_projects/           # LangFlow workflow definitions
│   └── enhanced_automation_flow.json
├── scripts/                     # Automation scripts
│   └── automation_control.sh    # Main control script
├── memory/                      # Automation data
│   ├── approval_queue.json      # Pending approvals
│   ├── pm_ledger.jsonl          # Event log
│   ├── automation.pid           # Process ID
│   └── automation.log           # System logs
├── Makefile.automation          # Enhanced build targets
└── docs/
    └── AUTOMATION_GUIDE.md      # This guide
```

## Configuration

### Environment Variables

The `scripts/automation_control.sh` script and other parts of the system can be configured using environment variables.

**LangFlow Server Configuration:**
These variables allow you to customize the host and port where the LangFlow server (started by `automation_control.sh`) will listen.
-   `LANGFLOW_HOST`: Defines the IP address or hostname for the LangFlow server.
    *   Default: `127.0.0.1`
    *   Example: `export LANGFLOW_HOST="0.0.0.0"` (to listen on all network interfaces)
-   `LANGFLOW_PORT`: Defines the port number for the LangFlow server.
    *   Default: `7860`
    *   Example: `export LANGFLOW_PORT="8000"`

```bash
# Example: Run LangFlow on a different port
export LANGFLOW_PORT="8080"
./scripts/automation_control.sh start
```

**Project Paths:**
While generally not needed to be overridden as they are dynamically determined, these illustrate internal path management.
```bash
# Project paths (typically auto-detected)
export PROJECT_ROOT="/path/to/barry-sharp-pro-mover"
```

**GB Studio CLI Path:**
This variable specifies the path to the `gb-studio-cli.js` executable.
-   Default: `gb-studio-cli` (script assumes it's in the system PATH)
-   Example: `export GBSTUDIO_CLI_PATH="/usr/local/gb-studio/gb-studio-cli.js"`
Refer to the "GB Studio CLI Dependency Management" section for more details.

**Logging Level for LangFlow:**
```bash
# Enable verbose logging for LangFlow components
export LANGFLOW_LOG_LEVEL=DEBUG
```

### File Watcher Settings

Edit `enhanced_file_watcher.py` to customize:
- Watched directories
- Ignore patterns
- Debounce timing
- Auto-trigger behavior

### CI/CD Pipeline Settings

Edit `ci_cd_pipeline.py` to customize:
- Validation steps
- Build targets
- Test procedures
- Deployment destinations
- Notification preferences

## Troubleshooting

### Common Issues

**Automation won't start:**
```bash
# Check dependencies
which langflow
which make
which python3

# Check logs
./scripts/automation_control.sh logs
```

**File watcher not detecting changes:**
```bash
# Check file permissions
ls -la assets/

# Verify watcher is running
./scripts/automation_control.sh status
```

**Build failures:**
```bash
# Test build manually
make build-rom

# Check validation
make check-bg check-scenes check-json
```

**LangFlow UI not accessible:**
```bash
# Check if port is in use
lsof -i :7860

# Try different port
LANGFLOW_PORT=7861 ./scripts/automation_control.sh start
```

### Log Files

- **System logs**: `memory/automation.log`
- **Event ledger**: `memory/pm_ledger.jsonl`
- **Approval queue**: `memory/approval_queue.json`

### Debug Mode

```bash
# Enable verbose logging
export LANGFLOW_LOG_LEVEL=DEBUG

# Run components directly
python3 langflow_components/ci_cd_pipeline.py
python3 langflow_components/enhanced_file_watcher.py
```

## Advanced Usage

### Custom Workflows

1. Create new LangFlow components in `langflow_components/`
2. Add them to the workflow in `langflow_projects/`
3. Update the control script if needed

### Integration with External Systems

- **Webhooks**: Add webhook triggers to the LangFlow workflow
- **Email notifications**: Extend the notifier component
- **Slack integration**: Add Slack webhook support
- **Git hooks**: Integrate with Git pre-commit/post-commit hooks

### Scaling

- **Multiple watchers**: Monitor different directories with separate watchers
- **Parallel builds**: Configure multiple build targets
- **Distributed deployment**: Deploy to multiple environments

## Best Practices

1. **Always test changes locally** before committing
2. **Monitor system resources** during automation runs
3. **Review approval queue regularly** to prevent backlog
4. **Keep logs clean** by rotating old log files
5. **Update documentation** when adding new components

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review system logs
3. Test components individually
4. Consult the LangFlow documentation

## Contributing

To contribute to the automation system:
1. Follow the existing code structure
2. Add comprehensive logging
3. Include error handling
4. Update documentation
5. Test thoroughly before submitting

## Repository Cleanup Notes

This section provides a brief overview of recent efforts to clarify the repository's structure and documentation, enhancing its usability for developers.

A review of the repository was conducted with the aim of improving overall clarity and making it easier for both new and existing developers to navigate and understand the project's components and workflows. The primary focus of this phase was on investigation and comprehensive documentation rather than on file deletion or architectural changes.

Key areas of clarification include:

*   **The `langflow/` Subdirectory:**
    *   New documentation (see "Understanding the `langflow/` Subdirectory" within the "Environment Setup" section) now clearly explains that this directory contains a full source code copy of the LangFlow application.
    *   It emphasizes that this embedded version is for reference or direct LangFlow development/debugging purposes and is **not** the version used by this project's automation pipelines. The project relies on LangFlow being installed as a package within the Python virtual environment (`venv/`).

*   **Utility Scripts (`scripts/` directory):**
    *   The `scripts/README.md` file has been updated and organized to provide clear descriptions, purposes, and usage instructions for key utility scripts. This includes scripts for project initialization (`bootstrap_pm_backbone.sh`), build and validation tests (`build/test_run_all.sh`, `build/test_validation.sh`), GB Studio asset metadata synchronization (`sync_gbsres.sh`), and quick Git snapshots (`snapshot.sh`).

*   **Custom Python Component Sources:**
    *   Clarifications have been added (see "A Note on Custom Python Component Sources" within the "Environment Setup" section) regarding the current setup for custom LangFlow Python components.
    *   This explains the role of the `.langflow/components/` directory for active/hot development, the function of `pyproject.toml` in defining the `barrysharp-components` package (which sources from `langflow_components/`), and how `pip install -e .` ties these together with LangFlow installation in the `venv/`.

The goal of these documentation updates is to reduce potential confusion and provide a clearer map for developers working with different aspects of this repository. No files were deleted as part of this specific cleanup and documentation effort; the focus was on enhancing understanding through improved documentation.