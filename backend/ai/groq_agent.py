"""
Groq AI Integration for Ultra-Fast Recommendations
Groq provides the fastest LLM inference (100x faster than Ollama)
"""

import json
import os
from typing import Dict, Optional
from dotenv import load_dotenv

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

load_dotenv()


class GroqAgent:
    """AI Agent using Groq API for lightning-fast recommendations"""
    
    DEFAULT_MODEL = "llama-3.1-8b-instant"  # Llama 3.1 8B Instant (fast!)
    
    # System prompt for recommendation generation
    SYSTEM_PROMPT = """You are an empathetic emotion support and social communication assistant. 
Your task is to provide helpful, actionable recommendations for someone experiencing an emotion or trying to communicate effectively.

For each request, provide 5-6 diverse recommendations including:
1. Social Replies: Suggestions for what to send to a partner, friend, or family member.
2. Relationship Insights: Predict how the recipient will feel if a specific message is sent.
3. Reply Analysis: If the user provided a message they received, analyze its emotion and suggest a reply.
4. Self-care & Activities: Practical actions for immediate emotional relief.

Keep responses concise, supportive, and practical. Use a warm, empathetic tone.
If the language is set to 'my', provide ALL text in Myanmar language (Burmese).
"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize Groq agent
        
        Args:
            api_key: Groq API key (or set GROQ_API_KEY env var)
            model: Groq model name (default: llama3-8b-8192)
        """
        if not GROQ_AVAILABLE:
            raise ImportError("Groq library not installed. Run: pip install groq")
        
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.model = model or os.getenv('GROQ_MODEL', self.DEFAULT_MODEL)
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set. Please set it in .env or environment.")
        
        self.client = Groq(api_key=self.api_key)
        self._is_available = None
    
    def is_available(self) -> bool:
        """Check if Groq API is accessible"""
        if self._is_available is not None:
            return self._is_available
        
        try:
            # Simple test call
            self.client.models.list()
            self._is_available = True
        except Exception:
            self._is_available = False
        
        return self._is_available
    
    def get_recommendations(self, emotion: str, context: str, language: str = 'en') -> Optional[Dict]:
        """
        Get AI-powered recommendations from Groq
        
        Args:
            emotion: Detected emotion
            context: User's input text for context
            language: 'en' for English, 'my' for Myanmar
            
        Returns:
            Dictionary with send_message and action, or None if AI fails
        """
        if not self.is_available():
            return None
        
        try:
            # Build prompt
            prompt = self._build_prompt(emotion, context, language)
            
            # Call Groq API (ultra-fast!)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200,
                timeout=10  # 10 second timeout
            )
            
            # Parse response
            content = response.choices[0].message.content
            recommendations = self._parse_response(content)
            
            if recommendations:
                return recommendations
            else:
                return None
                
        except Exception as e:
            print(f"Groq agent error: {e}")
            return None
    
    def _build_prompt(self, emotion: str, context: str, language: str = 'en') -> str:
        """Build prompt for LLM"""
        lang_instruction = "IMPORTANT: Provide all text in Myanmar (Burmese) language." if language == 'my' else "Provide all text in English."
        
        return f"""
User is feeling: {emotion.upper()}
Context/Message: "{context}"

{lang_instruction}

Provide 5-6 diverse recommendations in this JSON format:
{{
    "recommendations": [
        {{
            "type": "message",
            "label": "Send to partner/friend",
            "text": "suggested message text"
        }},
        {{
            "type": "impact",
            "label": "How they will feel",
            "text": "prediction of how the recipient will react to the message"
        }},
        {{
            "type": "reply_suggestion",
            "label": "Suggested Reply",
            "text": "how to reply if context is a received message"
        }},
        {{
            "type": "action",
            "label": "Activity",
            "text": "practical action to take"
        }},
        {{
            "type": "action",
            "label": "Self-care",
            "text": "self-care tip"
        }},
        {{
            "type": "action",
            "label": "Mindfulness",
            "text": "calming exercise"
        }}
    ]
}}

Only respond with valid JSON, no additional text.
"""
    
    def _parse_response(self, content: str) -> Optional[Dict]:
        """Parse LLM response to extract recommendations"""
        try:
            # Try to find JSON in response
            content = content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1])  # Remove ```json and ```
            
            # Parse JSON
            data = json.loads(content)
            
            # Handle new format with multiple recommendations
            if 'recommendations' in data and isinstance(data['recommendations'], list):
                return {
                    'recommendations': data['recommendations'],
                    'count': len(data['recommendations'])
                }
            
            # Fallback to old format (2 recommendations)
            if 'send_message' in data and 'action' in data:
                return {
                    'recommendations': [
                        {'type': 'message', 'label': 'Send Message', 'text': data['send_message']},
                        {'type': 'action', 'label': 'Self-Care Action', 'text': data['action']}
                    ],
                    'count': 2
                }
            
            return None
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to parse Groq response: {e}")
            return None

    def get_social_advice(self, message: str, perspective: str = 'receiver', language: str = 'en') -> Optional[Dict]:
        """
        Get social/relationship advice for a message
        """
        if not self.is_available():
            return None
            
        lang_name = "Myanmar (Burmese)" if language == 'my' else "English"
        
        if perspective == 'receiver':
            prompt = f"""
Analyze this message sent TO the user from someone else: "{message}"

1. What emotion is the sender likely feeling?
2. How should the user respond to be supportive/appropriate?
3. Provide 3 diverse reply options.

Respond in {lang_name} language in this JSON format:
{{
    "detected_emotion": "predicted emotion",
    "analysis": "brief explanation of sender's state",
    "advice": "general advice on how to handle",
    "suggested_replies": [
        "reply 1",
        "reply 2",
        "reply 3"
    ]
}}
Only respond with valid JSON.
"""
        else:
            prompt = f"""
Analyze this message the user wants to send TO someone else: "{message}"

1. How will the receiver likely feel when they read this?
2. Is this message appropriate?
3. Suggest 3 improved or alternative versions.

Respond in {lang_name} language in this JSON format:
{{
    "predicted_impact": "predicted emotion of receiver",
    "analysis": "brief explanation of how it might be perceived",
    "advice": "advice on whether to send or change",
    "suggested_replies": [
        "alternative 1",
        "alternative 2",
        "alternative 3"
    ]
}}
Only respond with valid JSON.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert relationship coach and emotion analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500,
                timeout=15
            )
            
            content = response.choices[0].message.content
            # Clean JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
                
            return json.loads(content.strip())
        except Exception as e:
            print(f"Social advice error: {e}")
            return None


# Singleton instance
_agent = None

def get_agent() -> GroqAgent:
    """Get or create GroqAgent singleton"""
    global _agent
    if _agent is None:
        try:
            _agent = GroqAgent()
        except Exception as e:
            print(f"Failed to initialize Groq agent: {e}")
            raise
    return _agent


def get_ai_recommendations(emotion: str, context: str, language: str = 'en') -> Optional[Dict]:
    """
    Convenience function to get AI recommendations
    
    Args:
        emotion: Detected emotion
        context: User's input text
        language: 'en' for English, 'my' for Myanmar
        
    Returns:
        Recommendation dictionary or None
    """
    try:
        return get_agent().get_recommendations(emotion, context, language)
    except Exception:
        return None


def get_social_advice(message: str, perspective: str = 'receiver', language: str = 'en') -> Optional[Dict]:
    """
    Convenience function to get social advice
    """
    try:
        return get_agent().get_social_advice(message, perspective, language)
    except Exception:
        return None


if __name__ == "__main__":
    # Test the agent
    print("Testing Groq AI Agent...")
    
    try:
        agent = GroqAgent()
        print(f"✅ Groq API available: {agent.is_available()}")
        
        if agent.is_available():
            test_cases = [
                ('joy', 'I just got promoted at work!'),
                ('anger', 'My friend cancelled plans last minute'),
                ('sadness', 'I miss my family who live far away'),
                ('fear', 'I have a big presentation tomorrow'),
                ('neutral', 'Just another regular day')
            ]
            
            for emotion, context in test_cases:
                print(f"\n{emotion.upper()}: {context}")
                rec = agent.get_recommendations(emotion, context)
                if rec:
                    print(f"  ✅ Send: {rec['send_message']}")
                    print(f"  ✅ Action: {rec['action']}")
                else:
                    print("  ❌ (Failed to get recommendations)")
                    
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("   Please set GROQ_API_KEY in .env file")
    except Exception as e:
        print(f"❌ Error: {e}")
