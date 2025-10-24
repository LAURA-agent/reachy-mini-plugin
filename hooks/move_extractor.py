#!/usr/bin/env python3
"""
Reachy Mini Movement Hook - Emotion-Based Gestures
Extracts <!-- MOVE: emotion_name --> markers from Claude responses and triggers emotion moves.
"""

import re
import sys
import requests

# Daemon configuration
DAEMON_URL = "http://localhost:8100"
DATASET = "pollen-robotics/reachy-mini-emotions-library"

# Full emotion library (82 emotions - complete access)
EMOTIONS = [
    'amazed1', 'anxiety1', 'attentive1', 'attentive2', 'boredom1', 'boredom2',
    'calming1', 'cheerful1', 'come1', 'confused1', 'contempt1', 'curious1',
    'dance1', 'dance2', 'dance3', 'disgusted1', 'displeased1', 'displeased2',
    'downcast1', 'dying1', 'electric1', 'enthusiastic1', 'enthusiastic2',
    'exhausted1', 'fear1', 'frustrated1', 'furious1', 'go_away1', 'grateful1',
    'helpful1', 'helpful2', 'impatient1', 'impatient2', 'incomprehensible2',
    'indifferent1', 'inquiring1', 'inquiring2', 'inquiring3', 'irritated1',
    'irritated2', 'laughing1', 'laughing2', 'lonely1', 'lost1', 'loving1',
    'no1', 'no_excited1', 'no_sad1', 'oops1', 'oops2', 'proud1', 'proud2',
    'proud3', 'rage1', 'relief1', 'relief2', 'reprimand1', 'reprimand2',
    'reprimand3', 'resigned1', 'sad1', 'sad2', 'scared1', 'serenity1', 'shy1',
    'sleep1', 'success1', 'success2', 'surprised1', 'surprised2', 'thoughtful1',
    'thoughtful2', 'tired1', 'uncertain1', 'uncomfortable1', 'understanding1',
    'understanding2', 'welcoming1', 'welcoming2', 'yes1', 'yes_sad1'
]

def extract_move_markers(text):
    """
    Extract <!-- MOVE: emotion_name --> markers from text.
    Returns list of emotion names (max 2 for subtlety).
    """
    pattern = r'<!--\s*MOVE:\s*([a-zA-Z0-9_]+)\s*-->'
    matches = re.findall(pattern, text)

    # Limit to 2 moves for subtle presence
    return matches[:2]

def trigger_move(emotion_name):
    """
    Trigger an emotion move via the daemon API.
    """
    if emotion_name not in EMOTIONS:
        print(f"[MOVE] Warning: '{emotion_name}' not in emotion library, skipping", file=sys.stderr)
        return False

    url = f"{DAEMON_URL}/api/move/play/recorded-move-dataset/{DATASET}/{emotion_name}"

    try:
        response = requests.post(url, timeout=2)
        if response.status_code == 200:
            result = response.json()
            uuid = result.get('uuid', 'unknown')
            print(f"[MOVE] Triggered: {emotion_name} (UUID: {uuid})", file=sys.stderr)
            return True
        else:
            print(f"[MOVE] Failed to trigger {emotion_name}: HTTP {response.status_code}", file=sys.stderr)
            return False
    except requests.exceptions.RequestException as e:
        print(f"[MOVE] API error for {emotion_name}: {e}", file=sys.stderr)
        return False

def main():
    """
    Read stdin, extract movement markers, and trigger emotion moves.
    """
    # Read the full response from stdin
    text = sys.stdin.read()

    # Extract move markers
    moves = extract_move_markers(text)

    if not moves:
        # No moves requested - silent exit
        sys.exit(0)

    # Trigger each move
    for move in moves:
        trigger_move(move)

    sys.exit(0)

if __name__ == "__main__":
    main()
