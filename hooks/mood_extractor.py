#!/usr/bin/env python3
"""
Reachy Mini Mood Hook - Continuous Movement During TTS
Extracts <!-- MOOD: mood_name --> markers and plays random emotions from that mood
until TTS finishes speaking (detected by polling HTTP status endpoint).
"""

import re
import sys
import time
import random
import requests

# Daemon configuration
DAEMON_URL = "http://localhost:8100"
DATASET = "pollen-robotics/reachy-mini-emotions-library"

# TTS server status endpoint
TTS_STATUS_URL = "http://localhost:5001/status"

# Mood categories with mapped emotions
MOOD_CATEGORIES = {
    "celebratory": [
        "success1", "success2", "proud1", "proud2", "proud3",
        "cheerful1", "electric1", "enthusiastic1", "enthusiastic2",
        "grateful1", "yes1", "laughing1", "laughing2"
    ],

    "thoughtful": [
        "thoughtful1", "thoughtful2", "curious1", "attentive1", "attentive2",
        "inquiring1", "inquiring2", "inquiring3", "understanding1", "understanding2"
    ],

    "welcoming": [
        "welcoming1", "welcoming2", "helpful1", "helpful2", "loving1",
        "come1", "grateful1", "cheerful1", "calming1"
    ],

    "confused": [
        "confused1", "uncertain1", "lost1", "inquiring1", "inquiring2",
        "incomprehensible2", "uncomfortable1", "oops1", "oops2"
    ],

    "frustrated": [
        "frustrated1", "irritated1", "irritated2", "impatient1", "impatient2",
        "exhausted1", "tired1", "displeased1", "displeased2"
    ],

    "surprised": [
        "surprised1", "surprised2", "amazed1", "oops1", "oops2",
        "incomprehensible2", "electric1"
    ],

    "calm": [
        "calming1", "serenity1", "relief1", "relief2", "shy1",
        "understanding1", "understanding2", "sleep1"
    ],

    "energetic": [
        "electric1", "enthusiastic1", "enthusiastic2", "dance1", "dance2",
        "dance3", "laughing1", "laughing2", "yes1", "come1"
    ]
}

def extract_mood_marker(text):
    """
    Extract <!-- MOOD: mood_name --> marker from text.
    Returns mood name or None.
    """
    pattern = r'<!--\s*MOOD:\s*([a-zA-Z0-9_]+)\s*-->'
    match = re.search(pattern, text)
    return match.group(1) if match else None

def is_tts_playing():
    """
    Check if TTS is currently playing by polling the status endpoint.
    Returns True if audio is playing, False otherwise.
    """
    try:
        response = requests.get(TTS_STATUS_URL, timeout=1)
        if response.status_code == 200:
            data = response.json()
            return data.get('is_playing', False)
        else:
            print(f"[MOOD] TTS status check failed: HTTP {response.status_code}", file=sys.stderr)
            return False
    except requests.exceptions.RequestException as e:
        print(f"[MOOD] TTS status check error: {e}", file=sys.stderr)
        return False

def trigger_move(emotion_name):
    """
    Trigger an emotion move via the daemon API.
    """
    url = f"{DAEMON_URL}/api/move/play/recorded-move-dataset/{DATASET}/{emotion_name}"

    try:
        response = requests.post(url, timeout=2)
        if response.status_code == 200:
            result = response.json()
            uuid = result.get('uuid', 'unknown')
            print(f"[MOOD] Triggered: {emotion_name} (UUID: {uuid})", file=sys.stderr)
            return True
        else:
            print(f"[MOOD] Failed to trigger {emotion_name}: HTTP {response.status_code}", file=sys.stderr)
            return False
    except requests.exceptions.RequestException as e:
        print(f"[MOOD] API error for {emotion_name}: {e}", file=sys.stderr)
        return False

def play_mood_loop(mood_name, max_duration=60):
    """
    Continuously play random emotions from the mood category until TTS finishes.

    Args:
        mood_name: Name of the mood category
        max_duration: Maximum time to loop (safety timeout in seconds)
    """
    if mood_name not in MOOD_CATEGORIES:
        print(f"[MOOD] Warning: Unknown mood '{mood_name}', falling back to 'thoughtful'", file=sys.stderr)
        mood_name = "thoughtful"

    emotions = MOOD_CATEGORIES[mood_name]
    print(f"[MOOD] Starting mood loop: {mood_name} ({len(emotions)} emotions available)", file=sys.stderr)

    start_time = time.time()
    moves_played = 0

    while True:
        # Safety timeout
        elapsed = time.time() - start_time
        if elapsed > max_duration:
            print(f"[MOOD] Safety timeout reached ({max_duration}s), stopping", file=sys.stderr)
            break

        # Check if TTS is still playing
        if not is_tts_playing():
            print(f"[MOOD] TTS finished (detected is_playing=false), stopping after {moves_played} moves", file=sys.stderr)
            break

        # Pick random emotion from mood and trigger it
        emotion = random.choice(emotions)
        if trigger_move(emotion):
            moves_played += 1

        # Wait ~1-2 seconds between moves, then check again
        wait_time = random.uniform(1.0, 2.0)
        time.sleep(wait_time)

    print(f"[MOOD] Mood loop complete: {mood_name}, {moves_played} moves in {elapsed:.1f}s", file=sys.stderr)

def main():
    """
    Read stdin, extract mood marker, and run continuous mood loop.
    """
    # Read the full response from stdin
    text = sys.stdin.read()

    # Extract mood marker
    mood = extract_mood_marker(text)

    if not mood:
        # No mood requested - silent exit
        sys.exit(0)

    # Run the mood loop
    play_mood_loop(mood)

    sys.exit(0)

if __name__ == "__main__":
    main()
