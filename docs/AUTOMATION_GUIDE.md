# Barry Sharp Pro Mover - Enhanced Automation Guide

This guide covers the enhanced automation system that provides continuous integration, deployment, and file monitoring capabilities for the Barry Sharp Pro Mover project.

## Overview

The enhanced automation system includes:

- **CI/CD Pipeline**: Automated build, test, and deployment
- **File Watcher**: Real-time monitoring of project files
- **LangFlow Integration**: Visual workflow management
- **Notification System**: Alerts for build status and changes
- **Status Reporting**: Comprehensive project health reports

## Quick Start

### 1. Install Dependencies

```bash
# Install LangFlow (if not already installed)
pip install langflow

# Install project dependencies
pip install -r requirements.txt  # if exists
```

### 2. Start the Automation System

```bash
# Using the control script
./scripts/automation_control.sh start

# Or using Make
make automation-start

# Or start development environment
make dev-start
```

### 3. Access the LangFlow UI

Open your browser to: http://127.0.0.1:7860

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

Direct integration with GB Studio CLI for ROM compilation.

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

The `scripts/automation_control.sh` script provides easy management of the automation system.

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

```bash
# LangFlow configuration
export LANGFLOW_HOST="127.0.0.1"
export LANGFLOW_PORT="7860"

# Project paths
export PROJECT_ROOT="/path/to/barry-sharp-pro-mover"
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