"""
Myanmar Language Emotion Detector
Supports Myanmar (Burmese) language emotion detection using LLM Agents.
Rule-based/keyword fallbacks have been removed.
"""

import re
from typing import Dict, List

# ─────────────────────────────────────────────────────────────────────────────
# Myanmar Unicode range: U+1000 – U+109F
# ─────────────────────────────────────────────────────────────────────────────

MYANMAR_UNICODE_RANGE = re.compile(r'[\u1000-\u109F\uAA60-\uAA7F\uA9E0-\uA9FF]')


def is_myanmar_text(text: str) -> bool:
    """
    Check if the text contains Myanmar Unicode characters.
    If 25% or more characters are Myanmar, returns True.
    """
    if not text:
        return False
    myanmar_chars = len(MYANMAR_UNICODE_RANGE.findall(text))
    total_chars = len([c for c in text if not c.isspace()])
    if total_chars == 0:
        return False
    return (myanmar_chars / total_chars) >= 0.25


# Emotion UI metadata (used by agents and frontends)
EMOTION_EMOJIS = {
    'joy': '😊',
    'anger': '😠',
    'sadness': '😢',
    'fear': '😨',
    'neutral': '😐',
}

EMOTION_COLORS = {
    'joy': 'green',
    'anger': 'red',
    'sadness': 'blue',
    'fear': 'purple',
    'neutral': 'gray',
}


def detect_myanmar_emotion(text: str) -> Dict:
    """
    Detect emotion from Myanmar text.
    1. Try Groq AI Agent first
    2. Try Ollama AI Agent second
    3. Return a clean offline neutral fallback if both are offline (no keyword fallback).

    Args:
        text: Myanmar input text

    Returns:
        Emotion detection result dict
    """
    # 1. Try Groq AI Agent
    try:
        from ai.groq_agent import get_agent as get_groq_agent
        groq_agent = get_groq_agent()
        if groq_agent.is_available():
            result = groq_agent.detect_emotion(text, language='my')
            if result:
                return result
    except Exception as e:
        print(f"⚠️ Groq Myanmar emotion detection failed: {e}")

    # 2. Try Ollama AI Agent
    try:
        from ai.ollama_agent import get_agent as get_ollama_agent
        ollama_agent = get_ollama_agent()
        if ollama_agent.is_available():
            result = ollama_agent.detect_emotion(text, language='my')
            if result:
                return result
    except Exception as e:
        print(f"⚠️ Ollama Myanmar emotion detection failed: {e}")

    # 3. Fallback to offline notice if both AI systems are unavailable
    return {
        'emotion': 'neutral',
        'confidence': 0.0,
        'emoji': EMOTION_EMOJIS['neutral'],
        'color': EMOTION_COLORS['neutral'],
        'language': 'my',
        'method': 'myanmar_llm_offline',
        'error': 'Myanmar emotion detection is currently offline. Please check your internet connection or start Ollama.',
        'scores': {
            'joy': 0.0,
            'sadness': 0.0,
            'anger': 0.0,
            'fear': 0.0,
            'neutral': 1.0
        }
    }


if __name__ == '__main__':
    print("Myanmar Emotion Detector (LLM-Only)")
    print("=" * 50)
    test_text = "ဒီနေ့ တော်တော် ပျော်တယ်"
    res = detect_myanmar_emotion(test_text)
    print(f"Text  : {test_text}")
    print(f"Result: {res}")
