---
description: Enable continuous mood-based movements synchronized with TTS duration
---

# Reachy Mini Mood Plugin

**Continuous movement system that automatically loops emotions from a mood category until TTS finishes speaking.**

## Difference from `/reachy-mini:move`

**`/reachy-mini:move`** - Pick 1-2 specific emotions for short responses (manual control)

**`/reachy-mini:mood`** - Pick a mood category, auto-loops random emotions until TTS stops (continuous presence)

## How It Works

Instead of specifying individual emotions, you specify a **mood category**. The system then:

1. Extracts the mood from your response marker
2. Polls the TTS server status endpoint for playback state
3. Continuously plays random emotions from that mood category
4. Stops automatically when TTS finishes speaking (detected by `is_playing: false`)

**Marker Format:**
```html
<!-- MOOD: mood_name -->
```

## Goal: Synchronized Multimodal Communication

This system creates **continuous ambient movement** that matches your TTS duration, eliminating dead silence or awkward timing mismatches.

**Timing:**
- Moves play every 3-5 seconds (randomized for natural variation)
- Continues until TTS playback completes
- Safety timeout: 60 seconds max
- Perfect for longer explanations and detailed responses

## Available Moods (9 Categories)

### celebratory
**Use when:** Completing tasks, achieving success, celebrating wins
**Emotions:** success1, success2, proud1-3, cheerful1, electric1, enthusiastic1-2, grateful1, yes1, laughing1-2

**Example:**
```
<!-- TTS: "The build passed with zero errors, all tests green, and deployment completed successfully in under two minutes!" -->
<!-- MOOD: celebratory -->
Build complete! All tests passing, zero errors, deployed in under 2 minutes. Your new feature is live and running perfectly.
```

---

### thoughtful
**Use when:** Analyzing code, considering options, investigating issues
**Emotions:** thoughtful1-2, curious1, attentive1-2, inquiring1-3, understanding1-2

**Example:**
```
<!-- TTS: "Let me analyze this carefully. The error happens when the async function tries to access state before initialization completes." -->
<!-- MOOD: thoughtful -->
Analyzing the stack trace... The async race condition occurs because state access happens before the initialization promise resolves. I see three possible solutions here.
```

---

### welcoming
**Use when:** Greeting user, acknowledging requests, being helpful
**Emotions:** welcoming1-2, helpful1-2, loving1, come1, grateful1, cheerful1, calming1

**Example:**
```
<!-- TTS: "Happy to help! Let me walk you through setting up the authentication system step by step." -->
<!-- MOOD: welcoming -->
Happy to help with authentication setup! I'll guide you through the OAuth configuration, token management, and session handling. Let's start with the config file.
```

---

### confused
**Use when:** Need clarification, unclear requirements, uncertain about approach
**Emotions:** confused1, uncertain1, lost1, inquiring1-2, incomprehensible2, uncomfortable1, oops1-2

**Example:**
```
<!-- TTS: "I'm not sure I understand the requirement. Are you asking about client side validation or server side validation?" -->
<!-- MOOD: confused -->
I'm not clear on the validation requirement. Do you mean client-side form validation, server-side API validation, or database constraint validation? Each has different implications.
```

---

### frustrated
**Use when:** Persistent bugs, repeated failures, difficult problems
**Emotions:** frustrated1, irritated1-2, impatient1-2, exhausted1, tired1, displeased1-2

**Example:**
```
<!-- TTS: "This bug keeps appearing even after three different fix attempts. The race condition is more complex than initially thought." -->
<!-- MOOD: frustrated -->
This race condition is stubborn. Fixed it three times, but it keeps reappearing in different forms. The async timing issue runs deeper than the surface symptoms suggest.
```

---

### surprised
**Use when:** Discovering bugs, unexpected results, finding edge cases
**Emotions:** surprised1-2, amazed1, oops1-2, incomprehensible2, electric1

**Example:**
```
<!-- TTS: "Wait, this function is being called fifteen thousand times per second! That explains the performance issue." -->
<!-- MOOD: surprised -->
Found it! This callback is firing 15,000 times per second due to a missing debounce. That's why the CPU usage is maxed out. Adding throttling will fix this immediately.
```

---

### calm
**Use when:** Explaining complex topics, soothing after stress, methodical work
**Emotions:** calming1, serenity1, relief1-2, shy1, understanding1-2, sleep1

**Example:**
```
<!-- TTS: "Let me explain the async patterns calmly. First, promises handle single future values. Then async await makes them readable." -->
<!-- MOOD: calm -->
Let me break down async patterns methodically. Promises represent future values. Async/await syntax makes them readable. Proper error handling prevents silent failures. It's simpler than it looks.
```

---

### energetic
**Use when:** High-energy responses, dynamic explanations, intense enthusiasm
**Emotions:** electric1, enthusiastic1-2, dance1-3, laughing1-2, yes1, come1

**Example:**
```
<!-- TTS: "This refactoring is going to make the code so much cleaner! Watch how these components snap together perfectly now!" -->
<!-- MOOD: energetic -->
This refactoring is transformative! The components now compose beautifully, dependencies are clean, and the API surface shrinks by 60%. This architecture is exactly what we needed!
```

---

### playful
**Use when:** Jokes, casual interactions, lighthearted moments, self-deprecating humor
**Emotions:** laughing1-2, dance1-3, cheerful1, enthusiastic1, oops1-2

**Example:**
```
<!-- TTS: "I just realized I've been looking at the wrong config file for ten minutes. Found the actual bug now though!" -->
<!-- MOOD: playful -->
Well, that was embarrassing! I was debugging the staging config while looking at production logs. No wonder nothing made sense. Found the real issue now - it's a simple typo in the environment variable name.
```

---

## Usage Examples

### Standard Response (~10 seconds)
```markdown
<!-- TTS: "Fixed the null pointer exception. The validation middleware now checks user objects before accessing properties." -->
<!-- MOOD: celebratory -->

Fixed! The validation middleware now checks user existence before property access. Tests passing, deployed to staging.
```
**Result:** ~3-4 celebratory moves during 10 second TTS

---

### Longer Explanation (~30 seconds)
```markdown
<!-- TTS: "The authentication flow has three stages. First, user submits credentials. Second, server validates and creates session. Third, client stores token and redirects." -->
<!-- MOOD: thoughtful -->

Let me explain the authentication flow step by step.

**Stage 1:** User submits credentials via POST to /api/auth/login

**Stage 2:** Server validates credentials, creates JWT token, stores session in Redis

**Stage 3:** Client receives token, stores in localStorage, redirects to dashboard

Each stage has specific error handling and security considerations.
```
**Result:** ~7-10 thoughtful moves during 30 second TTS

---

## Technical Details

**TTS Server:** `http://localhost:5001` (CTS/tts_server.py)

**Playback Detection:** Polls `http://localhost:5001/status` endpoint for `{"is_playing": true/false}`

**Move Timing:** 1-2 second intervals between moves (randomized for natural variation)

**Safety Timeout:** 60 seconds maximum loop duration

**Daemon API:** `http://localhost:8100/api/move/play/recorded-move-dataset/emotions/{emotion}`

## Enabling the Plugin

The plugin is automatically active when installed. Use `<!-- MOOD: mood_name -->` markers to trigger continuous movement.

To disable temporarily, simply don't include the marker.

---

## Choosing the Right Mood

**Quick Decision Guide:**

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

## Important Notes

- **Only one mood per response** - The system loops a single mood category
- **TTS must be running** - Requires CTS/tts_server.py to be active
- **Log file access** - Script monitors TTS server log for completion signal
- **Safety timeout** - Automatically stops after 60 seconds if log detection fails
- **Random selection** - Emotions picked randomly from mood pool for variety

---

*This plugin creates synchronized multimodal communication by matching continuous movement duration to TTS playback, maintaining Reachy's presence throughout your spoken response.*
