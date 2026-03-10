"""
Rule-based Recommendation Engine
Now uses Multi-Source Recommendation System
"""

from typing import Dict, List, Optional
from .multi_source_recommender import MultiSourceRecommender, get_recommender as get_multi_source_recommender


class RuleBasedRecommender:
    """Generate recommendations using multi-source rule-based system"""

    def __init__(self):
        """Initialize with multi-source recommender"""
        self.multi_source = get_multi_source_recommender()

    def get_recommendations(self, emotion: str, context: str = "") -> Dict:
        """
        Get multi-source recommendations based on emotion

        Args:
            emotion: Detected emotion (joy, anger, sadness, fear, neutral)
            context: Optional context text

        Returns:
            Dictionary with recommendations from multiple sources
        """
        # Get multi-source recommendations
        recs = self.multi_source.get_recommendations(
            emotion=emotion,
            context=context,
            source_types=['music', 'podcast', 'video', 'activity', 'self_care'],
            count=2
        )

        # Format for backward compatibility
        formatted = {
            'send_message': recs.get('send_message', "Reach out to someone you trust"),
            'action': recs.get('quick_action', {}).get('description', "Take a moment for yourself"),
            'sources': recs.get('sources', {}),
            'quick_action': recs.get('quick_action'),
            'emotion': recs.get('emotion', emotion)
        }

        return formatted

    def get_all_recommendations(self, emotion: str) -> Dict:
        """
        Get all available recommendations for an emotion

        Args:
            emotion: Emotion type

        Returns:
            Dictionary with all recommendation sources
        """
        return self.multi_source.get_recommendations(emotion, count=3)

    def get_quick_recommendation(self, emotion: str) -> Dict:
        """Get a single quick recommendation"""
        return self.multi_source.get_quick_recommendation(emotion)

    def get_all_sources(self) -> List[str]:
        """Get list of all available source types"""
        return self.multi_source.get_all_sources()


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
