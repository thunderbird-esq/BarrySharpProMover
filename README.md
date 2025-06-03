# Run LangFlow with Custom Components

This script automates the process of running LangFlow 1.4.2 with custom components.

## Prerequisites

1.  **LangFlow Virtual Environment:**
    *   Ensure you have a Python virtual environment set up for LangFlow.
    *   The script expects this environment to be located at `./langflow_env/`.
    *   If you haven't created one, you can do so with:
        ```bash
        python3 -m venv langflow_env
        ```
    *   Activate it:
        ```bash
        source langflow_env/bin/activate
        ```
    *   Install LangFlow 1.4.2 (and any other necessary packages) within this environment:
        ```bash
        pip install langflow==1.4.2
        ```
    *   Deactivate it for now:
        ```bash
        deactivate
        ```

2.  **Custom Components:**
    *   Place your custom LangFlow components in the following directory structure:
        `./.langflow/components/custom_components/`
    *   The `custom_components` directory should contain your component Python files (e.g., `my_component.py`).

## How to Run

1.  **Make the script executable (if not already):**
    ```bash
    chmod +x run_langflow.py
    ```

2.  **Execute the script:**
    ```bash
    ./run_langflow.py
    ```

The script will:
*   Activate the `./langflow_env/` virtual environment.
*   Set the `LANGFLOW_COMPONENTS_PATH` to point to your custom components directory.
*   Start LangFlow 1.4.2.

LangFlow should then be accessible in your web browser (usually at `http://127.0.0.1:7860`), and your custom components should be available in the LangFlow interface.
