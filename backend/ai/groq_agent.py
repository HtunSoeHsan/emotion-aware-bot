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
    SYSTEM_PROMPT = """You are an empathetic emotion support assistant. 
Your task is to provide helpful, actionable recommendations for someone experiencing an emotion.

For each request, provide exactly 2 recommendations:
1. A message they can send to another person (friend, family, colleague)
2. A self-care action they can take immediately

Keep responses concise, supportive, and practical.
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
    
    def get_recommendations(self, emotion: str, context: str) -> Optional[Dict]:
        """
        Get AI-powered recommendations from Groq
        
        Args:
            emotion: Detected emotion
            context: User's input text for context
            
        Returns:
            Dictionary with send_message and action, or None if AI fails
        """
        if not self.is_available():
            return None
        
        try:
            # Build prompt
            prompt = self._build_prompt(emotion, context)
            
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
    
    def _build_prompt(self, emotion: str, context: str) -> str:
        """Build prompt for LLM"""
        return f"""
User is feeling: {emotion.upper()}
Context: "{context}"

Provide exactly 2 recommendations in this JSON format:
{{
    "send_message": "suggested message to send to someone",
    "action": "self-care action to take"
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
            
            # Validate structure
            if 'send_message' in data and 'action' in data:
                return {
                    'send_message': data['send_message'],
                    'action': data['action']
                }
            
            return None
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to parse Groq response: {e}")
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


def get_ai_recommendations(emotion: str, context: str) -> Optional[Dict]:
    """
    Convenience function to get AI recommendations
    
    Args:
        emotion: Detected emotion
        context: User's input text
        
    Returns:
        Recommendation dictionary or None
    """
    try:
        return get_agent().get_recommendations(emotion, context)
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
