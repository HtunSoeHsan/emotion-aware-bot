"""
NLTK-based Emotion Detection using VADER Sentiment Analysis
MyanmarLanguage support added via myanmar_emotion_detector module.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import Dict, Tuple
from nlp.myanmar_emotion_detector import is_myanmar_text, detect_myanmar_emotion


class EmotionDetector:
    """Detect emotions from text using NLTK VADER"""
    
    # Emotion thresholds based on VADER compound score
    EMOTION_THRESHOLDS = {
        'joy': 0.6,        # compound >= 0.6
        'anger': -0.6,     # compound <= -0.6
        'sadness': -0.3,   # -0.6 < compound < -0.3
        'fear': 0.0,       # -0.3 < compound < 0
        'neutral': 0.3     # -0.3 < compound < 0.3
    }
    
    # Emotion emojis for UI
    EMOTION_EMOJIS = {
        'joy': '😊',
        'anger': '😠',
        'sadness': '😢',
        'fear': '😨',
        'neutral': '😐'
    }
    
    # Color codes for UI (Tailwind CSS)
    EMOTION_COLORS = {
        'joy': 'green',
        'anger': 'red',
        'sadness': 'blue',
        'fear': 'purple',
        'neutral': 'gray'
    }
    
    def __init__(self):
        """Initialize VADER sentiment analyzer"""
        self.analyzer = SentimentIntensityAnalyzer()
    
    def detect(self, text: str) -> Dict:
        """
        Detect emotion from text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with emotion, confidence, emoji, and color
        """
        # Get VADER sentiment scores
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Determine emotion based on compound score
        emotion, confidence = self._classify_emotion(compound)
        
        return {
            'emotion': emotion,
            'confidence': round(confidence, 2),
            'emoji': self.EMOTION_EMOJIS[emotion],
            'color': self.EMOTION_COLORS[emotion],
            'language': 'en',
            'scores': {
                'negative': round(scores['neg'], 3),
                'neutral': round(scores['neu'], 3),
                'positive': round(scores['pos'], 3),
                'compound': round(compound, 3)
            }
        }
    
    def _classify_emotion(self, compound: float) -> Tuple[str, float]:
        """
        Classify emotion based on compound score
        
        Returns:
            Tuple of (emotion, confidence)
        """
        if compound >= self.EMOTION_THRESHOLDS['joy']:
            # Joy: compound >= 0.6
            confidence = min(1.0, (compound - 0.6) / 0.4 + 0.5)
            return 'joy', confidence
        
        elif compound <= self.EMOTION_THRESHOLDS['anger']:
            # Anger: compound <= -0.6
            confidence = min(1.0, (abs(compound) - 0.6) / 0.4 + 0.5)
            return 'anger', confidence
        
        elif compound < self.EMOTION_THRESHOLDS['sadness']:
            # Sadness: -0.6 < compound < -0.3
            confidence = 0.5 + (abs(compound) - 0.3) / 0.3 * 0.5
            return 'sadness', confidence
        
        elif compound < self.EMOTION_THRESHOLDS['fear']:
            # Fear: -0.3 < compound < 0
            confidence = 0.5 - (compound / 0.3) * 0.5
            return 'fear', confidence
        
        elif compound < self.EMOTION_THRESHOLDS['neutral']:
            # Neutral: 0 <= compound < 0.3
            confidence = 0.5 + (0.3 - compound) / 0.3 * 0.5
            return 'neutral', confidence
        
        else:
            # Very close to zero = neutral
            return 'neutral', 0.5 - (compound / 0.3) * 0.5


# Singleton instance
_detector = None


def get_detector() -> EmotionDetector:
    """Get or create EmotionDetector singleton"""
    global _detector
    if _detector is None:
        _detector = EmotionDetector()
    return _detector


def detect_emotion(text: str) -> Dict:
    """
    Convenience function to detect emotion.
    Myanmar text ဖြစ်ပါက myanmar_emotion_detector ကို route လုပ်သည်။
    English text ဖြစ်ပါက VADER ကို သုံးသည်။

    Args:
        text: Input text (English or Myanmar)

    Returns:
        Emotion detection result dictionary
    """
    if is_myanmar_text(text):
        return detect_myanmar_emotion(text)
    return get_detector().detect(text)


if __name__ == "__main__":
    # Test the detector
    test_texts = [
        "I am so happy today!",
        "This makes me so angry!",
        "I feel really sad and lonely",
        "I'm worried about the future",
        "The weather is okay"
    ]
    
    detector = EmotionDetector()
    for text in test_texts:
        result = detector.detect(text)
        print(f"\nText: {text}")
        print(f"Emotion: {result['emoji']} {result['emotion']} ({result['confidence']:.2f})")
        print(f"Color: {result['color']}")
