# Run LangFlow with Custom Components

This script (`run_langflow.py`) automates the process of starting LangFlow 1.4.2 while ensuring it loads your custom components.

## Prerequisites

Before running the script, please ensure you have the following set up:

1.  **Python 3.x:**
    *   Ensure Python 3 (version 3.x) is installed on your system.

2.  **LangFlow Virtual Environment:**
    *   **Create the environment:** If you don't have one, create a dedicated Python virtual environment for LangFlow. This isolates its dependencies.
        ```bash
        python3 -m venv langflow_env
        ```
        This command creates a directory named `langflow_env` in your current location.
    *   **Activate the environment:**
        ```bash
        source langflow_env/bin/activate
        ```
    *   **Install LangFlow:** Once activated, install LangFlow version 1.4.2 within this environment.
        ```bash
        pip install langflow==1.4.2
        ```
    *   **(Optional) Deactivate for now:** After installation, you can deactivate the environment if you are not immediately running the script. The `run_langflow.py` script will handle activation.
        ```bash
        deactivate
        ```

3.  **Custom Components:**
    *   Create the necessary directory structure for your custom components if it doesn't already exist:
        `./.langflow/components/custom_components/`
    *   Place your custom LangFlow component Python files (e.g., `my_new_tool.py`, `another_custom_node.py`) directly inside the `custom_components` directory.

## How to Run the Script

1.  **Make the script executable:**
    If you haven't done so already, give the `run_langflow.py` script execute permissions. You only need to do this once.
    ```bash
    chmod +x run_langflow.py
    ```

2.  **Execute the script:**
    Run the script from your terminal:
    ```bash
    ./run_langflow.py
    ```

## What the Script Does

When you execute `./run_langflow.py`:

1.  It activates the Python virtual environment located at `./langflow_env/`.
2.  It sets the `LANGFLOW_COMPONENTS_PATH` environment variable to point to `./.langflow/components/custom_components/`. This tells LangFlow where to find your custom components.
3.  It starts LangFlow version 1.4.2.

LangFlow should then be accessible in your web browser (typically at `http://127.0.0.1:7860`), and your custom components should appear in the LangFlow user interface.
