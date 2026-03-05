"""
Rule-based Recommendation Engine
Fallback system when AI agent is unavailable
"""

from typing import Dict, List


class RuleBasedRecommender:
    """Generate recommendations using predefined rules"""
    
    # Emotion-specific recommendations
    RECOMMENDATIONS = {
        'joy': [
            {
                'send_message': "Share this happiness with someone! 🌟",
                'action': "Write this moment in your journal 📝"
            },
            {
                'send_message': "I'm having a great day! Hope you are too! ✨",
                'action': "Celebrate by doing something you love 🎉"
            },
            {
                'send_message': "Feeling amazing today! 💫",
                'action': "Take a photo to remember this feeling 📸"
            }
        ],
        'anger': [
            {
                'send_message': "I need some space right now",
                'action': "Take 5 deep breaths 🧘"
            },
            {
                'send_message': "Let's talk about this later when I'm calmer",
                'action': "Go for a short walk 🚶"
            },
            {
                'send_message': "I'm feeling frustrated and need time",
                'action': "Write down what's bothering you 📝"
            }
        ],
        'sadness': [
            {
                'send_message': "Can we talk? I'm not doing well",
                'action': "Call a friend or family member 📞"
            },
            {
                'send_message': "Having a tough day. Could use some support",
                'action': "Practice self-care: warm tea, cozy blanket ☕"
            },
            {
                'send_message': "I could really use a friend right now",
                'action': "Listen to uplifting music 🎵"
            }
        ],
        'fear': [
            {
                'send_message': "I'm feeling anxious about something",
                'action': "Practice grounding: 5-4-3-2-1 technique 🌿"
            },
            {
                'send_message': "Can you help me talk through my worries?",
                'action': "Do a quick meditation or breathing exercise 🧘"
            },
            {
                'send_message': "I'm nervous and could use some reassurance",
                'action': "Remind yourself: You've got this! 💪"
            }
        ],
        'neutral': [
            {
                'send_message': "Hey! How's your day going? 👋",
                'action': "Take a moment to appreciate the present 🌸"
            },
            {
                'send_message': "Just checking in! Hope you're doing well",
                'action': "Do something small that brings joy ☕"
            },
            {
                'send_message': "Having an okay day. How about you?",
                'action': "Stay positive and keep going! 🌟"
            }
        ]
    }
    
    def get_recommendations(self, emotion: str, context: str = "") -> Dict:
        """
        Get recommendations based on emotion
        
        Args:
            emotion: Detected emotion (joy, anger, sadness, fear, neutral)
            context: Optional context text (not used in rule-based, but kept for API compatibility)
            
        Returns:
            Dictionary with send_message and action
        """
        # Get recommendations for this emotion
        recs = self.RECOMMENDATIONS.get(emotion, self.RECOMMENDATIONS['neutral'])
        
        # Return first recommendation (can be enhanced with context matching)
        return recs[0]
    
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
