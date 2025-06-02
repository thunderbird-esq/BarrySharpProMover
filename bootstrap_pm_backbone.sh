#!/bin/bash

set -e

echo "=== [THUNDERBIRD.ESQ PM BACKBONE BOOTSTRAP] ==="
ROOT=$(pwd)

# Directories
DIRS=(
    "langflow_agents"
    "memory"
    "vectorstore"
    "docs"
    "feedback"
    "approved"
    "staging"
    "scripts"
    "langflow_components"
    "langflow_projects"
)

# Files and their content (parallel arrays)
FILES=(
    "langflow_agents/registry.json"
    "memory/approval_queue.json"
    "memory/pm_ledger.jsonl"
    "vectorstore/art_kb"
    "vectorstore/dialogue_kb"
    "vectorstore/music_kb"
    "vectorstore/code_kb"
    "vectorstore/qa_kb"
    "vectorstore/shared_kb"
    "docs/status_report_$(date +%Y%m%d).md"
    "staging/design_output.json"
    "scripts/snapshot.sh"
    "scripts/notify_cli.sh"
)

TEMPLATES=(
'{
  "agents": [
    {
      "name": "SpriteArtist",
      "type": "art",
      "description": "Handles all sprite and visual asset creation.",
      "memory_file": "../vectorstore/art_kb",
      "input_folder": "../assets/sprites/",
      "output_folder": "../assets/sprites/",
      "enabled": true
    },
    {
      "name": "DialogueWriter",
      "type": "dialogue",
      "description": "Creates and reviews dialogue scripts.",
      "memory_file": "../vectorstore/dialogue_kb",
      "input_folder": "../assets/dialogue/",
      "output_folder": "../assets/dialogue/",
      "enabled": true
    }
  ]
}
'
'{
  "queue": []
}
'
''
''
''
''
''
''
''
"# Status Report - $(date +%Y-%m-%d)\n\n"
'{}'
'#!/bin/bash
git add .
git commit -m "Snapshot: $1"
'
'#!/bin/bash
echo "[PM NOTIFY] $1"
'
)

# 1. Ensure directories exist
for DIR in "${DIRS[@]}"; do
    if [ ! -d "$DIR" ]; then
        mkdir -p "$DIR"
        echo "Created directory: $DIR"
    else
        echo "Directory exists: $DIR"
    fi
done

# 2. Ensure files exist and populate as needed
for IDX in "${!FILES[@]}"; do
    FILE="${FILES[$IDX]}"
    CONTENT="${TEMPLATES[$IDX]}"
    FILE_PATH="$FILE"

    # Bash variable interpolation for dates in filenames
    if [[ "$FILE_PATH" == *'$(date +%Y%m%d)'* ]]; then
        FILE_PATH=$(echo "$FILE_PATH" | sed "s/\$(date +%Y%m%d)/$(date +%Y%m%d)/g")
    fi
    if [[ "$FILE_PATH" == *'$(date +%Y-%m-%d)'* ]]; then
        FILE_PATH=$(echo "$FILE_PATH" | sed "s/\$(date +%Y-%m-%d)/$(date +%Y-%m-%d)/g")
    fi

    if [ ! -f "$FILE_PATH" ]; then
        # If script, make executable
        if [[ "$FILE_PATH" == scripts/*.sh ]]; then
            echo -e "$CONTENT" > "$FILE_PATH"
            chmod +x "$FILE_PATH"
            echo "Created script: $FILE_PATH"
        else
            echo -e "$CONTENT" > "$FILE_PATH"
            echo "Created file: $FILE_PATH"
        fi
    else
        echo "File exists: $FILE_PATH"
    fi
done

echo ""
echo "=== [PM BACKBONE CHECKLIST SUMMARY] ==="
for DIR in "${DIRS[@]}"; do
    [ -d "$DIR" ] && echo "✓ $DIR"
done
for IDX in "${!FILES[@]}"; do
    FILE="${FILES[$IDX]}"
    # Bash variable interpolation for dates in filenames
    if [[ "$FILE" == *'$(date +%Y%m%d)'* ]]; then
        FILE=$(echo "$FILE" | sed "s/\$(date +%Y%m%d)/$(date +%Y%m%d)/g")
    fi
    if [[ "$FILE" == *'$(date +%Y-%m-%d)'* ]]; then
        FILE=$(echo "$FILE" | sed "s/\$(date +%Y-%m-%d)/$(date +%Y-%m-%d)/g")
    fi
    [ -f "$FILE" ] && echo "✓ $FILE"
done

echo ""
echo "PM Backbone is READY for the Loaded PM flow."
echo "If you need to add or customize agent registry entries, edit: langflow_agents/registry.json"
echo "Ready for JSON import—next step is PM engine."

exit 0

