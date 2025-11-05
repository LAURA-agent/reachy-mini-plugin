---
description: Direct mood-based movements via daemon API (no conversation app required)
---

# Reachy Mini Mood Plugin (Direct Mode)

**Lightweight mood system that calls daemon API directly without requiring the conversation app.**

## Difference from `/reachy-mini:mood`

**`/reachy-mini:mood`** - Full integration with conversation app (requires run_reachy_pi.py)

**`/reachy-mini:mood-direct`** - Direct daemon API calls (only requires daemon running)

## When to Use This

Use **mood-direct** when:
- Testing mood behaviors without full conversation app
- Daemon is running but conversation app is not
- You want simpler, more predictable mood triggering
- Debugging mood system behavior

Use **mood** (regular) when:
- Full conversation app is running
- You want synchronized breathing/face tracking integration
- Running the complete Reachy Mini conversation system

## How It Works

This command uses the plugin's `mood_extractor.py` hook which:

1. Extracts `<!-- MOOD: mood_name -->` marker from your response
2. Polls TTS server status endpoint at `http://localhost:5001/status`
3. Continuously plays random emotions from that mood category
4. Stops when TTS finishes (`is_playing: false`)
5. Falls back to "thoughtful" mood if invalid mood specified

**Marker Format:**
```html
<!-- MOOD: mood_name -->
```

## Available Moods (9 Categories)

### celebratory
**Emotions:** success1, success2, proud1-3, cheerful1, electric1, enthusiastic1-2, grateful1, yes1, laughing1-2

### thoughtful
**Emotions:** thoughtful1-2, curious1, attentive1-2, inquiring1-3, understanding1-2

### welcoming
**Emotions:** welcoming1-2, helpful1-2, loving1, come1, grateful1, cheerful1, calming1

### confused
**Emotions:** confused1, uncertain1, lost1, inquiring1-2, incomprehensible2, uncomfortable1, oops1-2

### frustrated
**Emotions:** frustrated1, irritated1-2, impatient1-2, exhausted1, tired1, displeased1-2

### surprised
**Emotions:** surprised1-2, amazed1, oops1-2, incomprehensible2, electric1

### calm
**Emotions:** calming1, serenity1, relief1-2, shy1, understanding1-2, sleep1

### energetic
**Emotions:** electric1, enthusiastic1-2, dance1-3, laughing1-2, yes1, come1

### playful
**Emotions:** laughing1-2, dance1-3, cheerful1, enthusiastic1, oops1-2

## Usage Example

```markdown
<!-- TTS: "Fixed the bug! The validation middleware now handles edge cases properly." -->
<!-- MOOD: celebratory -->

Fixed! The validation middleware now checks all edge cases. Tests passing, ready for review.
```

## Technical Details

**Requirements:**
- Reachy Mini daemon running (`http://localhost:8100`)
- TTS server running (`http://localhost:5001`)

**Behavior:**
- Move timing: 1-2 second intervals between moves
- Safety timeout: 60 seconds maximum
- Fallback mood: "thoughtful" (if invalid mood specified)
- Dataset: `pollen-robotics/reachy-mini-emotions-library`

**No Integration With:**
- Conversation app breathing system
- Face tracking synchronization
- External control state management

## Quick Decision Guide

| **Situation** | **Mood** |
|--------------|----------|
| Task completed successfully | celebratory |
| Analyzing code/problem | thoughtful |
| Greeting/helping user | welcoming |
| Need clarification | confused |
| Persistent bug/difficulty | frustrated |
| Found unexpected issue | surprised |
| Explaining complex topic | calm |
| High-energy response | energetic |
| Jokes/casual/lighthearted | playful |

---

*This is the simplified direct-API version. For full integration with breathing and face tracking, use `/reachy-mini:mood` instead.*
