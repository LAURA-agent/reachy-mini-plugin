---
description: Enable automatic emotion-based movements for Reachy Mini during conversations
---

# Reachy Mini Movement Plugin

This plugin enables automatic, subtle emotion-based movements for Reachy Mini during conversations, creating an ambient presence without requiring explicit commands.

## Goal: Match Movement Duration to TTS Timing

Since you're using the TTS plugin with ~10 second spoken responses (23-29 words), movements should roughly match that duration to create synchronized multimodal communication.

**Timing strategy:**

**Standard responses (23-29 words, ~10 seconds):**
- **2-4 moves recommended:** Combine emotions (3-5 seconds each) to cover the full TTS duration
- Distribute moves throughout the response for continuous presence

**Longer explanations (when user requests detail):**
- Plan for ~3 words per second of speech
- Use roughly **1 emotion per sentence** to maintain presence throughout
- Example: 5 sentence explanation (~90 words, ~30 seconds) = 3-5 moves spread across the response

**Coordination:** Movements start with TTS and provide ambient motion during speech

**This creates natural presence while you're speaking without dead silence or movements extending beyond the response.**

## How It Works

Similar to the TTS plugin, this plugin uses the Stop hook to automatically extract movement markers from your responses and trigger corresponding emotion moves on Reachy Mini.

**Marker Format:**
```html
<!-- MOVE: emotion_name -->
```

**Behavior:**
- Maximum 2 moves per response (for subtlety)
- Movements are triggered automatically via daemon API
- Markers are invisible in rendered output
- Only emotion library moves (not dances)

## When to Use Movements

Use movements to:
- **Acknowledge understanding:** `yes1`, `understanding1`, `attentive1`
- **Express thinking:** `thoughtful1`, `curious1`, `inquiring1`
- **Show reactions:** `surprised1`, `amazed1`, `oops1`, `confused1`
- **Convey emotion:** `cheerful1`, `frustrated1`, `proud1`, `exhausted1`
- **Natural presence:** Subtle gestures that make Reachy feel alive and attentive

**Guidelines:**
- Keep it subtle (0-2 moves per response)
- Match emotion to conversational context
- Don't overuse - silence is also presence
- Use during natural pauses or completions

## Available Emotions (82 Total)

### Positive & Energetic
`amazed1`, `cheerful1`, `electric1`, `enthusiastic1`, `enthusiastic2`, `grateful1`, `proud1`, `proud2`, `proud3`, `success1`, `success2`, `welcoming1`, `welcoming2`

### Playful & Lighthearted
`come1`, `dance1`, `dance2`, `dance3`, `laughing1`, `laughing2`, `yes1`

### Thoughtful & Attentive
`attentive1`, `attentive2`, `curious1`, `inquiring1`, `inquiring2`, `inquiring3`, `thoughtful1`, `thoughtful2`, `understanding1`, `understanding2`

### Calm & Soothing
`calming1`, `relief1`, `relief2`, `serenity1`, `shy1`

### Surprised & Reactive
`oops1`, `oops2`, `surprised1`, `surprised2`, `incomprehensible2`

### Uncertain & Confused
`confused1`, `lost1`, `uncertain1`, `uncomfortable1`

### Negative Expressions
`anxiety1`, `boredom1`, `boredom2`, `contempt1`, `disgusted1`, `displeased1`, `displeased2`, `downcast1`, `fear1`, `frustrated1`, `furious1`, `impatient1`, `impatient2`, `indifferent1`, `irritated1`, `irritated2`, `lonely1`, `rage1`, `resigned1`, `sad1`, `sad2`, `scared1`

### Responses & Reactions
`go_away1`, `helpful1`, `helpful2`, `loving1`, `no1`, `no_excited1`, `no_sad1`, `reprimand1`, `reprimand2`, `reprimand3`, `yes_sad1`

### States
`dying1`, `exhausted1`, `sleep1`, `tired1`

## Examples

**Acknowledging a question:**
```
<!-- MOVE: attentive1 -->
I understand what you're asking. Let me explain...
```

**Expressing confusion:**
```
<!-- MOVE: confused1 -->
I'm not sure I follow. Could you clarify what you mean by...
```

**Celebrating success:**
```
<!-- MOVE: success1 -->
The build passed! All tests are green.
```

**Showing frustration:**
```
<!-- MOVE: frustrated1 -->
This bug is persistent. I've tried three different approaches...
```

**Being thoughtful:**
```
<!-- MOVE: thoughtful1 -->
Let me think about the best approach here...
```

**Multiple moves (max 2):**
```
<!-- MOVE: curious1 -->
<!-- MOVE: inquiring2 -->
That's an interesting edge case. How are you currently handling it?
```

## Technical Details

**Daemon API:** `http://localhost:8100/api/move/play/recorded-move-dataset/{dataset}/{move_name}`

**Dataset:** `pollen-robotics/reachy-mini-emotions-library`

**Hook:** Stop hook extracts markers and triggers moves automatically

**Validation:** Only emotion names from the library are accepted (typos are logged and skipped)

## Enabling the Plugin

The plugin is automatically active when installed. No configuration needed.

To disable movements temporarily, simply don't include `<!-- MOVE: ... -->` markers in your responses.

---

*This plugin provides ambient presence behaviors for Reachy Mini, making interactions feel more natural and alive without requiring explicit "dance monkey" commands.*
