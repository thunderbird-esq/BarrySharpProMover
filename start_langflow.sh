# start_langflow.sh
# This script starts the LangFlow server.
# Prerequisites:
# 1. LangFlow and its dependencies must be installed (e.g., via requirements.txt).
# 2. For flows utilizing Ollama, the Ollama service should be running.
# 3. Ensure this script has execute permissions (chmod +x start_langflow.sh).

#!/usr/bin/env bash

# Raise the soft limit for open file descriptors for this shell and child processes.
# This can be necessary for applications that handle many concurrent connections or files.
ulimit -n 8192

# Start LangFlow using exec to replace the shell process with the langflow process.
# --host: Binds LangFlow to the specified IP address. 127.0.0.1 means localhost.
# --port: Specifies the port LangFlow will listen on.
exec langflow run \
     --host 127.0.0.1 --port 7860
