#!/bin/bash

# Change to project root directory
cd "$(dirname "$0")/../../"

echo "🧪 Running GB Studio Validation..."

make check-bg || exit 1
make check-scenes || exit 1
make check-json || exit 1

echo "✅ All validation passed."