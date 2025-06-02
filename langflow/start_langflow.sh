#!/usr/bin/env bash
ulimit -n 8192
exec langflow run --host 127.0.0.1 --port 7860 --no-open-browser

