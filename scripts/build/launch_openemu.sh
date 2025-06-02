#!/bin/bash

# Change to project root directory
cd "$(dirname "$0")/../../"

ROM_PATH="./build/rom.gb"
OPENEMU_PATH="/Applications/OpenEmu.app"

if [ ! -f "$ROM_PATH" ]; then
  echo "❌ ROM not found at $ROM_PATH"
  exit 1
fi

if [ ! -d "$OPENEMU_PATH" ]; then
  echo "❌ OpenEmu not installed at $OPENEMU_PATH"
  exit 1
fi

open -a "$OPENEMU_PATH" "$ROM_PATH"