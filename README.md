# Reachy Mini Claude Code Plugin

**Automatic emotion-based movements for Reachy Mini robot during Claude Code conversations**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Reachy Mini](https://img.shields.io/badge/Reachy-Mini-orange.svg)](https://www.pollen-robotics.com/reachy-mini/)

---

## Overview

This Claude Code plugin enables Reachy Mini to automatically perform emotion-based movements synchronized with Claude's responses, creating natural multimodal communication without requiring explicit commands.

**Key Features:**
- 🎭 **82 emotion moves** from Pollen Robotics' official library
- 🎵 **TTS synchronization** - Continuous movements match speech duration
- 🎨 **8 mood categories** - Automatic emotion selection based on conversational context
- 🔄 **Two modes** - Single emotions or continuous mood loops
- 🤖 **Invisible markers** - HTML comments trigger movements without cluttering output

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Usage Modes](#usage-modes)
  - [Single Move Mode](#single-move-mode)
  - [Continuous Mood Mode](#continuous-mood-mode)
- [Available Emotions](#available-emotions)
- [Mood Categories](#mood-categories)
- [Integration with ElevenLabs TTS](#integration-with-elevenlabs-tts)
- [Technical Architecture](#technical-architecture)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Prerequisites

1. **Reachy Mini robot** with daemon running:
   ```bash
   mjpython -m reachy_mini.daemon.app.main --fastapi-port 8100
   ```

2. **Claude Code** installed and configured

3. **Python 3.8+** with `requests` library:
   ```bash
   pip install requests
   ```

### Install Plugin

1. Clone this repository into your Claude Code plugins directory:
   ```bash
   cd ~/.claude/plugins
   git clone https://github.com/LAURA-agent/reachy-mini-plugin.git reachy-mini
   ```

2. Restart Claude Code to load the plugin

3. Verify installation:
   ```bash
   # Plugin should appear in available plugins list
   ls ~/.claude/plugins/reachy-mini
   ```

---

## Quick Start

### Single Move Example

```markdown
<!-- MOVE: thoughtful1 -->
Let me analyze this code carefully...
```

**Result:** Reachy performs a thoughtful gesture once

### Continuous Mood Example

```markdown
<!-- TTS: "The build passed! All tests are green and deployment is complete." -->
<!-- MOOD: celebratory -->
Build successful! All tests passing, zero errors, deployed in under 2 minutes.
```

**Result:** Reachy continuously performs celebratory emotions (success, proud, cheerful) until TTS finishes speaking

---

## How It Works

The plugin uses **Stop hooks** to automatically detect and process movement markers in Claude's responses:

1. **Claude generates response** with embedded markers
2. **Stop hook fires** after response completes
3. **Extractors parse markers** from response text
4. **API calls trigger movements** on Reachy Mini daemon
5. **Movements execute** in sync with TTS (if using mood mode)

### Marker Format

**Single Move:**
```html
<!-- MOVE: emotion_name -->
```

**Continuous Mood:**
```html
<!-- MOOD: mood_category -->
```

Markers are **invisible in rendered output** - they only appear in the raw response text.

---

## Usage Modes

### Single Move Mode

**Use when:** Short responses, specific emotional reactions, precise control

**Command:** `/reachy-mini:move`

**Marker:** `<!-- MOVE: emotion_name -->`

**Behavior:**
- Maximum 2 moves per response (for subtlety)
- Triggers specific emotions from the 82-emotion library
- No TTS synchronization - fires immediately
- Best for quick reactions and acknowledgments

**Example:**
```markdown
<!-- MOVE: surprised1 -->
Found it! This callback is firing 15,000 times per second.
```

---

### Continuous Mood Mode

**Use when:** Longer explanations, sustained presence, TTS-synchronized communication

**Command:** `/reachy-mini:mood`

**Marker:** `<!-- MOOD: mood_category -->`

**Behavior:**
- Continuously loops random emotions from selected mood
- Polls TTS server for playback status
- Stops automatically when TTS finishes (`is_playing: false`)
- Safety timeout: 60 seconds maximum
- Best for detailed responses and explanations

**Example:**
```markdown
<!-- TTS: "Let me explain async patterns. Promises handle future values, async await makes them readable." -->
<!-- MOOD: thoughtful -->

Let me break down async patterns step by step:
- Promises represent future values
- Async/await makes them readable
- Proper error handling prevents silent failures
```

**Result:** Thoughtful emotions (thoughtful1, curious1, attentive1, etc.) play continuously during ~30 second TTS

---

## Available Emotions

**82 total emotions from Pollen Robotics library:**

### Positive & Energetic (13)
`amazed1`, `cheerful1`, `electric1`, `enthusiastic1`, `enthusiastic2`, `grateful1`, `proud1`, `proud2`, `proud3`, `success1`, `success2`, `welcoming1`, `welcoming2`

### Playful & Lighthearted (7)
`come1`, `dance1`, `dance2`, `dance3`, `laughing1`, `laughing2`, `yes1`

### Thoughtful & Attentive (10)
`attentive1`, `attentive2`, `curious1`, `inquiring1`, `inquiring2`, `inquiring3`, `thoughtful1`, `thoughtful2`, `understanding1`, `understanding2`

### Calm & Soothing (5)
`calming1`, `relief1`, `relief2`, `serenity1`, `shy1`

### Surprised & Reactive (5)
`oops1`, `oops2`, `surprised1`, `surprised2`, `incomprehensible2`

### Uncertain & Confused (4)
`confused1`, `lost1`, `uncertain1`, `uncomfortable1`

### Negative Expressions (22)
`anxiety1`, `boredom1`, `boredom2`, `contempt1`, `disgusted1`, `displeased1`, `displeased2`, `downcast1`, `fear1`, `frustrated1`, `furious1`, `impatient1`, `impatient2`, `indifferent1`, `irritated1`, `irritated2`, `lonely1`, `rage1`, `resigned1`, `sad1`, `sad2`, `scared1`

### Responses & Reactions (9)
`go_away1`, `helpful1`, `helpful2`, `loving1`, `no1`, `no_excited1`, `no_sad1`, `reprimand1`, `reprimand2`, `reprimand3`, `yes_sad1`

### States (4)
`dying1`, `exhausted1`, `sleep1`, `tired1`

---

## Mood Categories

### 1. celebratory
**Use when:** Completing tasks, achieving success, celebrating wins

**Emotions:** success1, success2, proud1-3, cheerful1, electric1, enthusiastic1-2, grateful1, yes1, laughing1-2

**Example:**
```markdown
<!-- TTS: "Build passed with zero errors!" -->
<!-- MOOD: celebratory -->
Build complete! All tests passing, deployed in under 2 minutes.
```

---

### 2. thoughtful
**Use when:** Analyzing code, considering options, investigating issues

**Emotions:** thoughtful1-2, curious1, attentive1-2, inquiring1-3, understanding1-2

**Example:**
```markdown
<!-- TTS: "Let me analyze this carefully..." -->
<!-- MOOD: thoughtful -->
Analyzing the stack trace... I see three possible solutions.
```

---

### 3. welcoming
**Use when:** Greeting user, acknowledging requests, being helpful

**Emotions:** welcoming1-2, helpful1-2, loving1, come1, grateful1, cheerful1, calming1

**Example:**
```markdown
<!-- TTS: "Happy to help!" -->
<!-- MOOD: welcoming -->
Happy to help with authentication setup! Let me guide you through it.
```

---

### 4. confused
**Use when:** Need clarification, unclear requirements, uncertain about approach

**Emotions:** confused1, uncertain1, lost1, inquiring1-2, incomprehensible2, uncomfortable1, oops1-2

**Example:**
```markdown
<!-- TTS: "I'm not sure I understand..." -->
<!-- MOOD: confused -->
I'm not clear on the validation requirement. Could you clarify?
```

---

### 5. frustrated
**Use when:** Persistent bugs, repeated failures, difficult problems

**Emotions:** frustrated1, irritated1-2, impatient1-2, exhausted1, tired1, displeased1-2

**Example:**
```markdown
<!-- TTS: "This bug keeps appearing..." -->
<!-- MOOD: frustrated -->
Fixed this three times, but it keeps coming back in different forms.
```

---

### 6. surprised
**Use when:** Discovering bugs, unexpected results, finding edge cases

**Emotions:** surprised1-2, amazed1, oops1-2, incomprehensible2, electric1

**Example:**
```markdown
<!-- TTS: "Wait, this function is being called fifteen thousand times per second!" -->
<!-- MOOD: surprised -->
Found it! This callback fires 15,000 times/sec - that's the CPU spike.
```

---

### 7. calm
**Use when:** Explaining complex topics, soothing after stress, methodical work

**Emotions:** calming1, serenity1, relief1-2, shy1, understanding1-2, sleep1

**Example:**
```markdown
<!-- TTS: "Let me explain this calmly..." -->
<!-- MOOD: calm -->
Let me break down async patterns methodically, step by step.
```

---

### 8. energetic
**Use when:** High-energy responses, playful interactions, dynamic explanations

**Emotions:** electric1, enthusiastic1-2, dance1-3, laughing1-2, yes1, come1

**Example:**
```markdown
<!-- TTS: "This refactoring is transformative!" -->
<!-- MOOD: energetic -->
This architecture is exactly what we needed! Components snap together perfectly!
```

---

## Integration with ElevenLabs TTS

The plugin is designed to work seamlessly with **ElevenLabs TTS** (or any TTS system with HTTP status API).

### How TTS Synchronization Works

1. **Claude generates response** with `<!-- MOOD: ... -->` marker
2. **TTS begins speaking** (via separate TTS plugin or system)
3. **Mood extractor starts polling** `http://localhost:5001/status` endpoint
4. **Reachy performs emotions** continuously while `{"is_playing": true}`
5. **Movement stops automatically** when `{"is_playing": false}`

### TTS Server Requirements

Your TTS server must expose a status endpoint:

**Endpoint:** `GET http://localhost:5001/status`

**Response format:**
```json
{
  "is_playing": true,  // or false when TTS completes
  "current_text": "...",
  "elapsed_time": 5.2
}
```

### Example TTS Integration

**Using the claude-to-speech plugin:**

```markdown
<!-- TTS: "The authentication system has three stages. First, user submits credentials..." -->
<!-- MOOD: thoughtful -->

Let me explain the authentication flow step by step.

**Stage 1:** User submits credentials via POST
**Stage 2:** Server validates and creates JWT token
**Stage 3:** Client stores token and redirects

Each stage has specific error handling.
```

**What happens:**
1. TTS plugin sends text to ElevenLabs API
2. ElevenLabs streams audio back (~30 seconds)
3. TTS server status shows `is_playing: true`
4. Mood extractor plays thoughtful emotions continuously
5. When audio completes, status changes to `is_playing: false`
6. Mood extractor stops automatically

### Timing Coordination

**Standard response (~10 seconds TTS):**
- 3-4 emotion moves (1-2 second intervals)
- Emotions spread throughout speech

**Longer explanation (~30 seconds TTS):**
- 7-10 emotion moves
- Natural variation via randomized timing

**Safety timeout:** 60 seconds maximum (prevents runaway loops if TTS status fails)

---

## Technical Architecture

### Plugin Structure

```
reachy-mini/
├── .claude-plugin/
│   ├── plugin.json           # Plugin metadata
│   └── marketplace.json      # Marketplace configuration
├── commands/
│   ├── move.md               # Single move mode documentation
│   └── mood.md               # Continuous mood mode documentation
├── hooks/
│   ├── hooks.json            # Hook configuration (Stop hook)
│   ├── stop.sh               # Main hook script
│   ├── move_extractor.py     # Single move marker extraction
│   ├── mood_extractor.py     # Continuous mood loop
│   └── mood_mapping.py       # Mood category definitions
├── README.md                 # This file
├── LICENSE                   # MIT license
└── requirements.txt          # Python dependencies
```

### Hook Execution Flow

```
Claude Response Generated
    ↓
Stop Hook Fires (hooks.json)
    ↓
stop.sh Executes
    ↓
Extracts Last Message from Transcript
    ↓
Passes to move_extractor.py (foreground)
    ↓
Passes to mood_extractor.py (background)
    ↓
Extractors Parse Markers
    ↓
API Calls to Reachy Daemon
    ↓
Movements Execute on Robot
```

### API Endpoints Used

**Reachy Mini Daemon:**
```
POST http://localhost:8100/api/move/play/recorded-move-dataset/{dataset}/{move_name}
```

**TTS Status (for mood mode):**
```
GET http://localhost:5001/status
```

---

## Configuration

### Daemon URL

**Default:** `http://localhost:8100`

**To change:** Edit `DAEMON_URL` in `hooks/move_extractor.py` and `hooks/mood_extractor.py`

### TTS Status URL

**Default:** `http://localhost:5001/status`

**To change:** Edit `TTS_STATUS_URL` in `hooks/mood_extractor.py`

### Movement Limits

**Single move mode:** Max 2 moves per response (configurable in `move_extractor.py`)

**Mood mode timeout:** 60 seconds (configurable via `max_duration` parameter)

### Mood Category Customization

Edit `MOOD_CATEGORIES` dict in `hooks/mood_extractor.py` to:
- Add new mood categories
- Modify emotion sets per mood
- Create custom mood combinations

---

## Troubleshooting

### Movements Not Triggering

**Check:**
1. Reachy Mini daemon is running: `curl http://localhost:8100/api/daemon/status`
2. Plugin is installed: `ls ~/.claude/plugins/reachy-mini`
3. Markers are properly formatted: `<!-- MOVE: emotion_name -->`
4. Check Claude Code logs for hook errors

**Debug:**
```bash
# Test move extraction manually
echo "<!-- MOVE: thoughtful1 -->" | python3 ~/.claude/plugins/reachy-mini/hooks/move_extractor.py
```

---

### Mood Loop Not Stopping

**Possible causes:**
1. TTS server not responding to status checks
2. TTS status endpoint returning incorrect data
3. Network connectivity issues

**Solutions:**
- Verify TTS server: `curl http://localhost:5001/status`
- Check mood_extractor.py logs for TTS polling errors
- Safety timeout (60s) will eventually stop the loop

---

### Invalid Emotion Names

**Symptom:** Warning in logs: `'emotion_name' not in emotion library`

**Cause:** Typo in emotion name or unsupported emotion

**Solution:** Check available emotions list in this README or `move_extractor.py`

---

### API Connection Errors

**Symptom:** `API error for emotion_name: Connection refused`

**Cause:** Daemon not running or wrong port

**Solution:**
```bash
# Start daemon if not running
mjpython -m reachy_mini.daemon.app.main --fastapi-port 8100

# Or adjust DAEMON_URL in extractor scripts
```

---

## Requirements

### Python Dependencies

See `requirements.txt`:
```
requests>=2.31.0
```

Install with:
```bash
pip install -r requirements.txt
```

### System Requirements

- **Reachy Mini** robot with daemon v1.0+
- **Claude Code** 2.0+
- **Python** 3.8+
- **TTS server** (optional, for mood mode only)

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Test with real Reachy Mini hardware when possible
- Follow PEP 8 style guide for Python code
- Update documentation for new features
- Add emotion names to library list when Pollen Robotics releases new moves

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Pollen Robotics** for Reachy Mini and emotion library
- **Anthropic** for Claude Code plugin system
- **LAURA Project** for integration development

---

## Related Projects

- [Reachy Mini SDK](https://github.com/pollen-robotics/reachy_mini) - Official Reachy Mini Python SDK
- [claude-to-speech](https://github.com/LAURA-agent/claude-to-speech) - TTS plugin for Claude Code
- [LAURA Project](https://github.com/LAURA-agent) - Full multimodal AI assistant system

---

## Support

For questions or issues:
- Open an issue on GitHub
- Contact: LAURA-agent organization
- Reachy Mini support: [Pollen Robotics](https://www.pollen-robotics.com/support/)

---

*Making Reachy Mini come alive through natural, emotion-driven movement during conversations.*
