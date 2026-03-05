"""
Ollama LLM Integration for Smart Recommendations
Provides contextual, personalized recommendations using local LLM
"""

import json
import ollama
from typing import Dict, Optional
from dotenv import load_dotenv
import os

load_dotenv()


class OllamaAgent:
    """AI Agent using Ollama for smart recommendations"""
    
    DEFAULT_MODEL = "llama2:latest"  # Use your installed llama2 model
    DEFAULT_HOST = "http://localhost:11434"
    
    # System prompt for recommendation generation
    SYSTEM_PROMPT = """You are an empathetic emotion support assistant. 
Your task is to provide helpful, actionable recommendations for someone experiencing an emotion.

For each request, provide exactly 2 recommendations:
1. A message they can send to another person (friend, family, colleague)
2. A self-care action they can take immediately

Keep responses concise, supportive, and practical.
"""
    
    def __init__(self, model: str = None, host: str = None):
        """
        Initialize Ollama agent
        
        Args:
            model: Ollama model name (default: llama2:7b)
            host: Ollama server host (default: http://localhost:11434)
        """
        self.model = model or os.getenv('OLLAMA_MODEL', self.DEFAULT_MODEL)
        self.host = host or os.getenv('OLLAMA_HOST', self.DEFAULT_HOST)
        self.client = ollama.Client(host=self.host)
        self._is_available = None
    
    def is_available(self) -> bool:
        """Check if Ollama server is reachable"""
        if self._is_available is not None:
            return self._is_available
        
        try:
            self.client.list()
            self._is_available = True
        except Exception:
            self._is_available = False
        
        return self._is_available
    
    def get_recommendations(self, emotion: str, context: str) -> Optional[Dict]:
        """
        Get AI-powered recommendations
        
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
            
            # Call Ollama
            response = self.client.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.SYSTEM_PROMPT},
                    {'role': 'user', 'content': prompt}
                ]
            )
            
            # Parse response
            content = response['message']['content']
            recommendations = self._parse_response(content)
            
            if recommendations:
                return recommendations
            else:
                return None
                
        except Exception as e:
            print(f"Ollama agent error: {e}")
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
            print(f"Failed to parse LLM response: {e}")
            return None


# Singleton instance
_agent = None


def get_agent() -> OllamaAgent:
    """Get or create OllamaAgent singleton"""
    global _agent
    if _agent is None:
        _agent = OllamaAgent()
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
    return get_agent().get_recommendations(emotion, context)


if __name__ == "__main__":
    # Test the agent
    agent = OllamaAgent()
    
    print(f"Ollama available: {agent.is_available()}")
    
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
                print(f"  Send: {rec['send_message']}")
                print(f"  Action: {rec['action']}")
            else:
                print("  (AI failed, would use fallback)")
