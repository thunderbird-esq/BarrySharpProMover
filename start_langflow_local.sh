#!/bin/bash

# Define paths
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
LANGFLOW_REPO_DIR="$PROJECT_DIR/langflow_repo"
VENV_DIR="$PROJECT_DIR/langflow_env"

# Function to print messages
log() {
    echo "[INFO] $1"
}

error() {
    echo "[ERROR] $1" >&2
    exit 1
}

# Check if langflow_repo exists, if not clone it
if [ ! -d "$LANGFLOW_REPO_DIR" ]; then
    log "Langflow repository not found. Cloning..."
    git clone https://github.com/langflow-ai/langflow.git "$LANGFLOW_REPO_DIR" || error "Failed to clone Langflow repository."
else
    log "Langflow repository found at $LANGFLOW_REPO_DIR"
fi

# Check if virtual environment exists, if not create it
if [ ! -d "$VENV_DIR" ]; then
    log "Python virtual environment not found. Creating..."
    python3 -m venv "$VENV_DIR" || error "Failed to create Python virtual environment."
    touch "$VENV_DIR/newly_created" # Add marker here
else
    log "Python virtual environment found at $VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate" || error "Failed to activate Python virtual environment."
log "Python virtual environment activated."

# Navigate to langflow_repo
cd "$LANGFLOW_REPO_DIR" || error "Failed to navigate to $LANGFLOW_REPO_DIR"

# Install/Update backend dependencies if pyproject.toml has changed or uv.lock is missing
# (Simplified check: just install if .venv is newly created or uv.lock missing)
# A more robust check would involve comparing timestamps or checksums
if [ ! -f "uv.lock" ] || [ -f "$VENV_DIR/newly_created" ]; then # Check for a marker or if uv.lock is missing
    log "Installing backend dependencies..."
    make install_backend || error "Failed to install backend dependencies."
    # Remove the marker after successful installation
    if [ -f "$VENV_DIR/newly_created" ]; then
        rm "$VENV_DIR/newly_created"
    fi
    touch "$VENV_DIR/backend_installed"
else
    log "Backend dependencies appear to be installed."
fi

# Install/Update frontend dependencies if package-lock.json has changed or node_modules missing
# (Simplified check: just install if node_modules is missing)
if [ ! -d "src/frontend/node_modules" ]; then
    log "Installing frontend dependencies..."
    make install_frontend || error "Failed to install frontend dependencies."
else
    log "Frontend dependencies appear to be installed."
fi

# Build frontend if build directory is missing
if [ ! -d "src/backend/base/langflow/frontend/assets" ]; then
    log "Building frontend..."
    make build_frontend || error "Failed to build frontend."
else
    log "Frontend appears to be built."
fi

log "Starting Langflow backend..."
# Start backend in the background
make backend &
BACKEND_PID=$!
log "Backend PID: $BACKEND_PID"

log "Starting Langflow frontend..."
# Start frontend in the background
make frontend &
FRONTEND_PID=$!
log "Frontend PID: $FRONTEND_PID"

log "Langflow started successfully."
log "Backend is running with PID $BACKEND_PID"
log "Frontend is running with PID $FRONTEND_PID"
log "Access Langflow at http://127.0.0.1:3000 (frontend dev server) or http://127.0.0.1:7860 (backend API)"

# Wait for backend and frontend to exit (optional, for script to keep running)
wait $BACKEND_PID
wait $FRONTEND_PID
