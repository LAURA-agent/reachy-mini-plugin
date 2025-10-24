#!/bin/bash
#
# Reachy Mini Stop Hook - Automatic Movement Triggers
# Fires after Claude finishes responding
# Extracts and triggers movement markers from response
#

# Get the plugin directory (parent of hooks directory)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

# Path to extractor scripts
MOVE_SCRIPT="$PLUGIN_DIR/hooks/move_extractor.py"
MOOD_SCRIPT="$PLUGIN_DIR/hooks/mood_extractor.py"

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

        # Run mood extractor (for continuous mood loops) in background
        # This allows mood loop to run while we return control
        echo "$RESPONSE" | python3 "$MOOD_SCRIPT" 2>&1 &
    fi
fi

exit 0
