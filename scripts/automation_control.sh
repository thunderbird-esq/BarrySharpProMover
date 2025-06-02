#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Automation Control Script for Barry Sharp Pro Mover
# Manages the enhanced CI/CD and file monitoring automation system
# ---------------------------------------------------------------------------

set -euo pipefail

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LANGFLOW_HOST="127.0.0.1"
LANGFLOW_PORT="7860"
PIDFILE="$PROJECT_ROOT/memory/automation.pid"
LOGFILE="$PROJECT_ROOT/memory/automation.log"
COMPONENTS_DIR="$PROJECT_ROOT/langflow_components"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Utility functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $1${NC}"
}

# Check if automation is running
is_running() {
    if [[ -f "$PIDFILE" ]]; then
        local pid=$(cat "$PIDFILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        else
            rm -f "$PIDFILE"
            return 1
        fi
    fi
    return 1
}

# Start the automation system
start_automation() {
    log "Starting Barry Sharp Pro Mover automation system..."
    
    if is_running; then
        log_warning "Automation system is already running (PID: $(cat "$PIDFILE"))"
        return 0
    fi
    
    # Ensure directories exist
    mkdir -p "$(dirname "$PIDFILE")"
    mkdir -p "$(dirname "$LOGFILE")"
    
    # Check dependencies
    if ! command -v langflow &> /dev/null; then
        log_error "LangFlow is not installed or not in PATH"
        return 1
    fi
    
    if ! command -v make &> /dev/null; then
        log_error "Make is not installed or not in PATH"
        return 1
    fi
    
    # Install/update custom components
    log "Installing custom LangFlow components..."
    if [[ -f "$COMPONENTS_DIR/import_nodes.py" ]]; then
        cd "$PROJECT_ROOT"
        python3 "$COMPONENTS_DIR/import_nodes.py" || log_warning "Failed to install some components"
    fi
    
    # Start LangFlow in background
    log "Starting LangFlow server on $LANGFLOW_HOST:$LANGFLOW_PORT..."
    cd "$PROJECT_ROOT"
    
    # Use the existing start script if available, otherwise start directly
    if [[ -f "start_langflow.sh" ]]; then
        nohup ./start_langflow.sh > "$LOGFILE" 2>&1 &
    else
        nohup langflow run --host "$LANGFLOW_HOST" --port "$LANGFLOW_PORT" > "$LOGFILE" 2>&1 &
    fi
    
    local langflow_pid=$!
    echo "$langflow_pid" > "$PIDFILE"
    
    # Wait a moment for LangFlow to start
    sleep 5
    
    # Verify LangFlow is running
    if ! ps -p "$langflow_pid" > /dev/null 2>&1; then
        log_error "Failed to start LangFlow. Check log: $LOGFILE"
        rm -f "$PIDFILE"
        return 1
    fi
    
    # Test connection
    local retries=10
    while [[ $retries -gt 0 ]]; do
        if curl -s "http://$LANGFLOW_HOST:$LANGFLOW_PORT/health" > /dev/null 2>&1; then
            break
        fi
        log "Waiting for LangFlow to be ready... ($retries retries left)"
        sleep 2
        ((retries--))
    done
    
    if [[ $retries -eq 0 ]]; then
        log_error "LangFlow failed to become ready"
        stop_automation
        return 1
    fi
    
    log_success "Automation system started successfully!"
    log "LangFlow UI: http://$LANGFLOW_HOST:$LANGFLOW_PORT"
    log "PID: $langflow_pid"
    log "Logs: $LOGFILE"
    
    # Start file watcher if available
    start_file_watcher
}

# Stop the automation system
stop_automation() {
    log "Stopping Barry Sharp Pro Mover automation system..."
    
    if ! is_running; then
        log_warning "Automation system is not running"
        return 0
    fi
    
    local pid=$(cat "$PIDFILE")
    
    # Stop file watcher first
    stop_file_watcher
    
    # Stop LangFlow
    log "Stopping LangFlow (PID: $pid)..."
    kill "$pid" 2>/dev/null || true
    
    # Wait for graceful shutdown
    local retries=10
    while [[ $retries -gt 0 ]] && ps -p "$pid" > /dev/null 2>&1; do
        sleep 1
        ((retries--))
    done
    
    # Force kill if necessary
    if ps -p "$pid" > /dev/null 2>&1; then
        log_warning "Force killing LangFlow process..."
        kill -9 "$pid" 2>/dev/null || true
    fi
    
    rm -f "$PIDFILE"
    log_success "Automation system stopped"
}

# Start file watcher
start_file_watcher() {
    log "Starting enhanced file watcher..."
    
    if [[ -f "$COMPONENTS_DIR/enhanced_file_watcher.py" ]]; then
        cd "$PROJECT_ROOT"
        nohup python3 "$COMPONENTS_DIR/enhanced_file_watcher.py" >> "$LOGFILE" 2>&1 &
        local watcher_pid=$!
        echo "$watcher_pid" > "$PROJECT_ROOT/memory/watcher.pid"
        log_success "File watcher started (PID: $watcher_pid)"
    else
        log_warning "Enhanced file watcher not found"
    fi
}

# Stop file watcher
stop_file_watcher() {
    local watcher_pidfile="$PROJECT_ROOT/memory/watcher.pid"
    
    if [[ -f "$watcher_pidfile" ]]; then
        local watcher_pid=$(cat "$watcher_pidfile")
        if ps -p "$watcher_pid" > /dev/null 2>&1; then
            log "Stopping file watcher (PID: $watcher_pid)..."
            kill "$watcher_pid" 2>/dev/null || true
            sleep 2
            if ps -p "$watcher_pid" > /dev/null 2>&1; then
                kill -9 "$watcher_pid" 2>/dev/null || true
            fi
        fi
        rm -f "$watcher_pidfile"
    fi
}

# Get automation status
get_status() {
    echo "=== Barry Sharp Pro Mover Automation Status ==="
    echo
    
    if is_running; then
        local pid=$(cat "$PIDFILE")
        log_success "Automation system is RUNNING (PID: $pid)"
        
        # Check LangFlow health
        if curl -s "http://$LANGFLOW_HOST:$LANGFLOW_PORT/health" > /dev/null 2>&1; then
            log_success "LangFlow server is responding"
            echo "  URL: http://$LANGFLOW_HOST:$LANGFLOW_PORT"
        else
            log_warning "LangFlow server is not responding"
        fi
        
        # Check file watcher
        local watcher_pidfile="$PROJECT_ROOT/memory/watcher.pid"
        if [[ -f "$watcher_pidfile" ]]; then
            local watcher_pid=$(cat "$watcher_pidfile")
            if ps -p "$watcher_pid" > /dev/null 2>&1; then
                log_success "File watcher is running (PID: $watcher_pid)"
            else
                log_warning "File watcher is not running"
                rm -f "$watcher_pidfile"
            fi
        else
            log_warning "File watcher status unknown"
        fi
        
    else
        log_error "Automation system is NOT RUNNING"
    fi
    
    echo
    echo "=== Recent Activity ==="
    if [[ -f "$LOGFILE" ]]; then
        echo "Last 10 log entries:"
        tail -n 10 "$LOGFILE" | sed 's/^/  /'
    else
        echo "No log file found"
    fi
    
    echo
    echo "=== System Resources ==="
    echo "Disk usage: $(df -h "$PROJECT_ROOT" | tail -1 | awk '{print $5}') of $(df -h "$PROJECT_ROOT" | tail -1 | awk '{print $2}')"
    echo "Memory usage: $(ps -o pid,ppid,pcpu,pmem,comm -p $$ 2>/dev/null | tail -1 | awk '{print $4}')%"
}

# Run CI/CD pipeline manually
run_pipeline() {
    log "Triggering CI/CD pipeline manually..."
    
    if ! is_running; then
        log_error "Automation system is not running. Start it first with: $0 start"
        return 1
    fi
    
    # Run the pipeline directly
    if [[ -f "$COMPONENTS_DIR/ci_cd_pipeline.py" ]]; then
        cd "$PROJECT_ROOT"
        python3 "$COMPONENTS_DIR/ci_cd_pipeline.py"
    else
        log_error "CI/CD pipeline component not found"
        return 1
    fi
}

# Generate status report
generate_report() {
    log "Generating status report..."
    
    if [[ -f "$COMPONENTS_DIR/report_gen.py" ]]; then
        cd "$PROJECT_ROOT"
        python3 "$COMPONENTS_DIR/report_gen.py"
        
        # Find the most recent report
        local report_file=$(find docs/ -name "status_report_*.md" -type f -exec ls -t {} + | head -1 2>/dev/null)
        if [[ -n "$report_file" ]]; then
            log_success "Report generated: $report_file"
            echo
            echo "=== Report Preview ==="
            head -20 "$report_file" | sed 's/^/  /'
            echo "  ..."
        fi
    else
        log_error "Report generator not found"
        return 1
    fi
}

# Show usage
show_usage() {
    echo "Barry Sharp Pro Mover Automation Control"
    echo
    echo "Usage: $0 {start|stop|restart|status|pipeline|report|logs|help}"
    echo
    echo "Commands:"
    echo "  start     - Start the automation system (LangFlow + file watcher)"
    echo "  stop      - Stop the automation system"
    echo "  restart   - Restart the automation system"
    echo "  status    - Show automation system status"
    echo "  pipeline  - Manually trigger CI/CD pipeline"
    echo "  report    - Generate status report"
    echo "  logs      - Show recent logs"
    echo "  help      - Show this help message"
    echo
    echo "Files:"
    echo "  PID file: $PIDFILE"
    echo "  Log file: $LOGFILE"
    echo "  Components: $COMPONENTS_DIR"
}

# Show logs
show_logs() {
    if [[ -f "$LOGFILE" ]]; then
        echo "=== Automation Logs (last 50 lines) ==="
        tail -n 50 "$LOGFILE"
    else
        log_warning "No log file found at $LOGFILE"
    fi
}

# Main command handling
case "${1:-help}" in
    start)
        start_automation
        ;;
    stop)
        stop_automation
        ;;
    restart)
        stop_automation
        sleep 2
        start_automation
        ;;
    status)
        get_status
        ;;
    pipeline)
        run_pipeline
        ;;
    report)
        generate_report
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        log_error "Unknown command: $1"
        echo
        show_usage
        exit 1
        ;;
esac