#!/bin/bash
#
# Reachy Mini Stop Hook - Automatic Movement Triggers
# Fires after Claude finishes responding
# Extracts and triggers movement markers from response
#

# Debug logging
DEBUG_FILE="/tmp/reachy_mini_stop_hook.log"
echo "=== Reachy Mini Stop Hook Fired at $(date) ===" >> "$DEBUG_FILE"

# Get the plugin directory (parent of hooks directory)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

# Path to extractor scripts
MOVE_SCRIPT="$PLUGIN_DIR/hooks/move_extractor.py"
MOOD_SCRIPT="/home/user/reachy/pi_reachy_deployment/mood_extractor.py"

# Read the JSON input from stdin
INPUT=$(cat)

# Extract the transcript path from JSON
TRANSCRIPT_PATH=$(echo "$INPUT" | grep -o '"transcript_path":"[^"]*"' | cut -d'"' -f4)

# Read the last assistant message from the transcript
if [ -f "$TRANSCRIPT_PATH" ]; then
    # Get the last line (latest message) from the transcript
    LAST_MESSAGE=$(tail -1 "$TRANSCRIPT_PATH")

    # Extract content from the JSON - content is an array of objects
    RESPONSE=$(echo "$LAST_MESSAGE" | python3 -c "
import sys, json
try:
    msg = json.load(sys.stdin)
    content = msg.get('message', {}).get('content', [])
    if isinstance(content, list) and len(content) > 0:
        # Get the first text block
        for block in content:
            if block.get('type') == 'text':
                print(block.get('text', ''))
                break
except:
    pass
" 2>/dev/null || echo "")

    # Pass response to both extractors (move and mood)
    if [ -n "$RESPONSE" ]; then
        # Run move extractor (for specific emotions)
        echo "$RESPONSE" | python3 "$MOVE_SCRIPT" 2>&1

        # Extract mood marker from response
        MOOD=$(echo "$RESPONSE" | grep -oP '<!--\s*MOOD:\s*\K[a-zA-Z0-9_]+(?=\s*-->)' | head -1)

        # If mood marker found, POST to conversation app to trigger mood state
        if [ -n "$MOOD" ]; then
            echo "Found mood marker: $MOOD" >> "$DEBUG_FILE"
            curl -s -X POST http://localhost:8888/mood/trigger \
                -H "Content-Type: application/json" \
                -d "{\"mood\":\"$MOOD\"}" >> "$DEBUG_FILE" 2>&1 &
        fi
    fi
fi

exit 0
