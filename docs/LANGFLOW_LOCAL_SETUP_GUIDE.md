# Langflow Local Development Setup Guide for LLM Collaborators

This guide explains how to set up and run Langflow locally for development and collaboration using the provided `start_langflow_local.sh` script. Please follow these instructions carefully to ensure a smooth experience.

## Prerequisites

Before you begin, ensure you have the following installed on your system (macOS):

*   **Git**: For cloning the Langflow repository.
*   **Python 3.9+**: Langflow requires a compatible Python version. The script will create a virtual environment.
*   **Make**: The Langflow repository uses a `Makefile` for various build and run commands, which our script utilizes.

## How to Start Langflow

1.  **Navigate to the project root directory** in your terminal:
    ```bash
    cd /path/to/your/BARRY-SHARP-PRO-MOVER-1
    ```
2.  **Run the startup script**:
    ```bash
    ./start_langflow_local.sh
    ```
    If you get a permission denied error, make the script executable first:
    ```bash
    chmod +x ./start_langflow_local.sh
    ./start_langflow_local.sh
    ```

3.  **Access Langflow**:
    *   **Frontend (UI)**: Open your web browser and go to <mcurl name="http://localhost:3000/" url="http://localhost:3000/"/>
    *   **Backend API**: The backend API will be running at <mcurl name="http://127.0.0.1:7860/" url="http://127.0.0.1:7860/"/>

## What the `start_langflow_local.sh` Script Does

The script automates the following steps:

1.  **Checks for `langflow_repo`**: If the `langflow_repo/` directory (containing the cloned Langflow source code) doesn't exist in the project root, it clones the official Langflow repository into it.
2.  **Checks for `langflow_env`**: If the `langflow_env/` Python virtual environment directory doesn't exist, it creates it.
3.  **Activates Virtual Environment**: It activates the `langflow_env`.
4.  **Installs Dependencies**: If the virtual environment was newly created or dependencies are missing, it installs backend (Python) and frontend (Node.js) dependencies using `make install_backend` and `make install_frontend` from within `langflow_repo/`.
5.  **Builds Frontend**: If the frontend hasn't been built, it runs `make build_frontend`.
6.  **Starts Services**: It starts the Langflow backend and frontend development server in the background using `make run_backend` and `make run_frontend` respectively.

## IMPORTANT: What You SHOULD NOT DO

To avoid breaking the setup or causing conflicts, please adhere to the following:

*   **DO NOT manually delete `langflow_repo/` or `langflow_env/`** unless you intend to completely reset the Langflow setup. The script is designed to manage these directories.
*   **DO NOT commit `langflow_repo/` or `langflow_env/` to Git.** These are local development directories and should be ignored by Git. They are (or should be) listed in the project's `.gitignore` file.
    *   `langflow_repo/` is the full source code of Langflow, which is external.
    *   `langflow_env/` contains local Python packages and can be very large.
*   **DO NOT run `make init`, `make install_backend`, `make install_frontend`, `make build_frontend`, `make run_backend`, or `make run_frontend` directly from within the `langflow_repo/` directory *unless you fully understand the Makefile and the purpose of the `start_langflow_local.sh` script*. The script provides a controlled environment and sequence for these operations.
*   **DO NOT change the default port numbers** (backend: 7860, frontend dev server: 3000) unless you are prepared to update configurations in the `Makefile` or relevant `.env` files within `langflow_repo/`. The script and default Langflow setup expect these ports.
*   **DO NOT modify files directly within `langflow_repo/` unless you are an advanced user contributing to Langflow itself.** For creating custom components, follow the official Langflow documentation and place your custom components in the designated project directories (e.g., `your_project_root/.langflow/components/`).

## How to Stop Langflow

The `start_langflow_local.sh` script starts the backend and frontend processes in the background. To stop them:

1.  **Find the Process IDs (PIDs)**:
    You can typically find the processes by looking for `uvicorn` (backend) and `vite` (frontend) or by the ports they use.
    ```bash
    # Find backend process (listening on port 7860)
    lsof -i :7860
    # Find frontend process (listening on port 3000)
    lsof -i :3000
    ```
    Alternatively, you can try:
    ```bash
    ps aux | grep uvicorn # For backend
    ps aux | grep vite    # For frontend
    ```
2.  **Kill the Processes**:
    Once you have the PIDs, use the `kill` command:
    ```bash
    kill <PID_for_backend>
    kill <PID_for_frontend>
    ```
    If a simple `kill` doesn't work, you might need to use `kill -9 <PID>` (force kill).

    *Note: The `start_langflow_local.sh` script attempts to kill existing processes when it starts, but this might not always be perfectly clean, especially for the frontend due to how the `Makefile` handles it.*

## Troubleshooting Common Messages

During startup, you might see these messages in the terminal. They are generally benign:

*   **`kill: usage: kill ...` followed by `make[1]: [run_frontend] Error 1 (ignored)`**:
    This occurs when the `Makefile` tries to stop a previous frontend server that isn't running. It's ignored, and the new server starts correctly.
*   **`warning: \`VIRTUAL_ENV=...\` does not match the project environment path \`.venv\`...`**:
    This is a warning from `uv` (the Python package manager). It indicates that our virtual environment (`langflow_env/`) is not named `.venv` as `uv` might prefer for auto-detection within `langflow_repo/`. However, the script correctly activates `langflow_env/`, and Langflow functions as expected.

If you encounter other issues, please document the steps you took and any error messages received.
