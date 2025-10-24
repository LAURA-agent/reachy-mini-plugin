"""
Mood Mapping for Reachy Mini Emotion Clusters

Maps high-level moods to clusters of emotion moves for ambient presence during TTS.
"""

# Mood clusters - each mood contains a list of related emotions
MOOD_CLUSTERS = {
    'thoughtful': [
        'thoughtful1', 'thoughtful2', 'curious1', 'inquiring1', 'inquiring2',
        'inquiring3', 'attentive1', 'attentive2', 'understanding1', 'understanding2'
    ],

    'energetic': [
        'cheerful1', 'enthusiastic1', 'enthusiastic2', 'electric1', 'success1',
        'success2', 'proud1', 'proud2', 'proud3', 'amazed1', 'yes1'
    ],

    'playful': [
        'laughing1', 'laughing2', 'dance1', 'dance2', 'dance3', 'come1',
        'electric1', 'oops1', 'oops2'
    ],

    'calm': [
        'calming1', 'serenity1', 'relief1', 'relief2', 'understanding1',
        'understanding2', 'welcoming1', 'welcoming2', 'grateful1'
    ],

    'confused': [
        'confused1', 'uncertain1', 'lost1', 'oops1', 'oops2',
        'incomprehensible2', 'uncomfortable1'
    ],

    'frustrated': [
        'frustrated1', 'impatient1', 'impatient2', 'irritated1', 'irritated2',
        'exhausted1', 'tired1', 'resigned1', 'displeased1', 'displeased2'
    ],

    'sad': [
        'sad1', 'sad2', 'downcast1', 'lonely1', 'no_sad1', 'yes_sad1',
        'resigned1', 'uncomfortable1'
    ],

    'surprised': [
        'surprised1', 'surprised2', 'amazed1', 'oops1', 'oops2',
        'incomprehensible2', 'fear1', 'scared1'
    ],

    'angry': [
        'furious1', 'rage1', 'frustrated1', 'irritated1', 'irritated2',
        'contempt1', 'disgusted1', 'reprimand1', 'reprimand2', 'reprimand3'
    ],

    'helpful': [
        'helpful1', 'helpful2', 'welcoming1', 'welcoming2', 'grateful1',
        'understanding1', 'understanding2', 'attentive1', 'attentive2', 'yes1'
    ],

    'shy': [
        'shy1', 'uncertain1', 'uncomfortable1', 'downcast1', 'anxiety1'
    ],

    'sleepy': [
        'sleep1', 'tired1', 'exhausted1', 'boredom1', 'boredom2', 'resigned1'
    ],

    'affectionate': [
        'loving1', 'grateful1', 'welcoming1', 'welcoming2', 'cheerful1',
        'shy1', 'come1'
    ],

    'defiant': [
        'no1', 'no_excited1', 'go_away1', 'contempt1', 'reprimand1',
        'reprimand2', 'reprimand3', 'indifferent1'
    ],

    'neutral': [
        'attentive1', 'attentive2', 'thoughtful1', 'curious1', 'yes1',
        'understanding1', 'calming1', 'serenity1'
    ]
}

def get_mood_emotions(mood_name):
    """
    Get the list of emotions for a given mood.

    Args:
        mood_name: Name of the mood (e.g., 'thoughtful', 'energetic')

    Returns:
        List of emotion names, or None if mood not found
    """
    return MOOD_CLUSTERS.get(mood_name.lower())

def get_all_moods():
    """
    Get list of all available mood names.

    Returns:
        List of mood names
    """
    return list(MOOD_CLUSTERS.keys())

def validate_mood(mood_name):
    """
    Check if a mood name is valid.

    Args:
        mood_name: Name to validate

    Returns:
        True if valid, False otherwise
    """
    return mood_name.lower() in MOOD_CLUSTERS
