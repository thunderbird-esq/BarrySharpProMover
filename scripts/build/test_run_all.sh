#!/bin/bash
set -e

# Change to project root directory
cd "$(dirname "$0")/../../"

# Run validation checks
make check-bg
make check-scenes
make check-json

# Build processes
make build-rom
make build-web
make hash-rom

echo "✅ Full GB Studio pipeline complete."