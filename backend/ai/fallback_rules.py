"""
Rule-based Recommendation Engine
Fallback system when AI agent is unavailable
"""

from typing import Dict, List


class RuleBasedRecommender:
    """Generate recommendations using predefined rules"""
    
    # Emotion-specific recommendations (expanded to 5 per emotion)
    RECOMMENDATIONS = {
        'joy': [
            {'type': 'message', 'label': 'Send to friend', 'text': "Share this happiness with someone! 🌟"},
            {'type': 'message', 'label': 'Send to family', 'text': "I'm having a great day! Hope you are too! ✨"},
            {'type': 'action', 'label': 'Document moment', 'text': "Write this moment in your journal 📝"},
            {'type': 'action', 'label': 'Celebrate', 'text': "Celebrate by doing something you love 🎉"},
            {'type': 'action', 'label': 'Capture memory', 'text': "Take a photo to remember this feeling 📸"}
        ],
        'anger': [
            {'type': 'message', 'label': 'Send to person', 'text': "I need some space right now"},
            {'type': 'message', 'label': 'Send later', 'text': "Let's talk about this later when I'm calmer"},
            {'type': 'action', 'label': 'Breathing', 'text': "Take 5 deep breaths 🧘"},
            {'type': 'action', 'label': 'Physical', 'text': "Go for a short walk 🚶"},
            {'type': 'action', 'label': 'Express', 'text': "Write down what's bothering you 📝"}
        ],
        'sadness': [
            {'type': 'message', 'label': 'Send to friend', 'text': "Can we talk? I'm not doing well"},
            {'type': 'message', 'label': 'Send to family', 'text': "Having a tough day. Could use some support"},
            {'type': 'action', 'label': 'Connect', 'text': "Call a friend or family member 📞"},
            {'type': 'action', 'label': 'Self-care', 'text': "Practice self-care: warm tea, cozy blanket ☕"},
            {'type': 'action', 'label': 'Mood boost', 'text': "Listen to uplifting music 🎵"}
        ],
        'fear': [
            {'type': 'message', 'label': 'Send to someone', 'text': "I'm feeling anxious about something"},
            {'type': 'message', 'label': 'Ask for help', 'text': "Can you help me talk through my worries?"},
            {'type': 'action', 'label': 'Grounding', 'text': "Practice grounding: 5-4-3-2-1 technique 🌿"},
            {'type': 'action', 'label': 'Calm', 'text': "Do a quick meditation or breathing exercise 🧘"},
            {'type': 'action', 'label': 'Affirmation', 'text': "Remind yourself: You've got this! 💪"}
        ],
        'neutral': [
            {'type': 'message', 'label': 'Check in', 'text': "Hey! How's your day going? 👋"},
            {'type': 'message', 'label': 'Connect', 'text': "Just checking in! Hope you're doing well"},
            {'type': 'action', 'label': 'Mindfulness', 'text': "Take a moment to appreciate the present 🌸"},
            {'type': 'action', 'label': 'Small joy', 'text': "Do something small that brings joy ☕"},
            {'type': 'action', 'label': 'Motivation', 'text': "Stay positive and keep going! 🌟"}
        ]
    }
    
    def get_recommendations(self, emotion: str, context: str = "") -> Dict:
        """
        Get recommendations based on emotion
        
        Args:
            emotion: Detected emotion (joy, anger, sadness, fear, neutral)
            context: Optional context text (not used in rule-based, but kept for API compatibility)
            
        Returns:
            Dictionary with recommendations array and count
        """
        # Get recommendations for this emotion
        recs = self.RECOMMENDATIONS.get(emotion, self.RECOMMENDATIONS['neutral'])
        
        # Return all recommendations
        return {
            'recommendations': recs,
            'count': len(recs)
        }
    
    def get_all_recommendations(self, emotion: str) -> List[Dict]:
        """
        Get all available recommendations for an emotion
        
        Args:
            emotion: Emotion type
            
        Returns:
            List of all recommendation pairs
        """
        return self.RECOMMENDATIONS.get(emotion, self.RECOMMENDATIONS['neutral'])


# Singleton instance
_recommender = None


def get_recommender() -> RuleBasedRecommender:
    """Get or create RuleBasedRecommender singleton"""
    global _recommender
    if _recommender is None:
        _recommender = RuleBasedRecommender()
    return _recommender


def get_recommendations(emotion: str, context: str = "") -> Dict:
    """
    Convenience function to get recommendations
    
    Args:
        emotion: Detected emotion
        context: Optional context
        
    Returns:
        Recommendation dictionary
    """
    return get_recommender().get_recommendations(emotion, context)


if __name__ == "__main__":
    # Test the recommender
    recommender = RuleBasedRecommender()
    
    for emotion in ['joy', 'anger', 'sadness', 'fear', 'neutral']:
        print(f"\n{emotion.upper()}:")
        rec = recommender.get_recommendations(emotion)
        print(f"  Send: {rec['send_message']}")
        print(f"  Action: {rec['action']}")
