"""
Ollama LLM Integration for Smart Recommendations
Provides contextual, personalized recommendations using local LLM
"""

import json
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
from typing import Dict, Optional
from dotenv import load_dotenv
import os

load_dotenv()


class OllamaAgent:
    """AI Agent using Ollama for smart recommendations"""
    
    DEFAULT_MODEL = "llama2:latest"  # Use your installed llama2 model
    DEFAULT_HOST = "http://localhost:11434"
    
    # System prompt for recommendation generation
    SYSTEM_PROMPT = """You are an empathetic emotional support assistant. 
Your task is to provide helpful, actionable recommendations for someone experiencing an emotion.

For each request, provide 2-3 diverse recommendations focusing solely on:
1. Mindfulness: Short calming exercises or breathing techniques.
2. Daily Exercise: Active physical or mental tasks to soothe or celebrate the emotion.

Do NOT include any general activities, activity cards, self-care tips/advice, social replies, relationship advice, or messages to send to others.
Keep responses concise, supportive, and practical. Use a warm, empathetic tone.
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
        if OLLAMA_AVAILABLE:
            self.client = ollama.Client(host=self.host)
        else:
            self.client = None
        self._is_available = None
    
    def is_available(self) -> bool:
        """Check if Ollama server is reachable"""
        if not OLLAMA_AVAILABLE or self.client is None:
            self._is_available = False
            return False
            
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

    def detect_emotion(self, text: str, language: str = 'my') -> Optional[Dict]:
        """
        Classify emotion of text using Ollama LLM
        
        Args:
            text: Text to analyze
            language: Language of the input text
            
        Returns:
            Dictionary with emotion, confidence, emoji, color, scores, language, method
        """
        if not self.is_available():
            return None
        
        prompt = f"""
You are a precise emotion classification assistant. Analyze the emotion of the following text:
"{text}"

Classify the text into one of these 5 emotions: 'joy', 'sadness', 'anger', 'fear', 'neutral'.

Here are some examples of Myanmar (Burmese) text classification:
Text: "ဒီနေ့ တော်တော် ပျော်တယ်"
Classification: {{
    "emotion": "joy",
    "confidence": 0.95,
    "scores": {{
        "joy": 0.95,
        "sadness": 0.01,
        "anger": 0.01,
        "fear": 0.01,
        "neutral": 0.02
    }}
}}

Text: "ငါ့ဘဝကြီးက အရမ်းပင်ပန်းလွန်းလို့ ငိုချင်တယ်"
Classification: {{
    "emotion": "sadness",
    "confidence": 0.90,
    "scores": {{
        "joy": 0.01,
        "sadness": 0.90,
        "anger": 0.03,
        "fear": 0.03,
        "neutral": 0.03
    }}
}}

Text: "ဒီပစ္စည်းက ပျက်စီးနေတယ်၊ တော်တော်စိတ်တိုဖို့ကောင်းတယ်"
Classification: {{
    "emotion": "anger",
    "confidence": 0.95,
    "scores": {{
        "joy": 0.01,
        "sadness": 0.02,
        "anger": 0.95,
        "fear": 0.01,
        "neutral": 0.01
    }}
}}

Text: "ရှေ့ဆက်ပြီး ဘာဖြစ်လာမလဲဆိုတာ တွေးပြီး တုန်လှုပ်ခြောက်ခြားနေမိတယ်"
Classification: {{
    "emotion": "fear",
    "confidence": 0.92,
    "scores": {{
        "joy": 0.01,
        "sadness": 0.02,
        "anger": 0.02,
        "fear": 0.92,
        "neutral": 0.03
    }}
}}

Text: "စားပွဲပေါ်မှာ စာအုပ်တစ်အုပ် ရှိတယ်"
Classification: {{
    "emotion": "neutral",
    "confidence": 0.98,
    "scores": {{
        "joy": 0.00,
        "sadness": 0.01,
        "anger": 0.00,
        "fear": 0.01,
        "neutral": 0.98
    }}
}}

Text: "မပျော်တာတော့ မဟုတ်ပါဘူး"
Classification: {{
    "emotion": "joy",
    "confidence": 0.70,
    "scores": {{
        "joy": 0.70,
        "sadness": 0.05,
        "anger": 0.05,
        "fear": 0.05,
        "neutral": 0.15
    }}
}}

Respond ONLY with a JSON object for the target text. Do not include markdown code block formatting (like ```json), introduction, or explanation.
"""
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': 'You are a precise emotion classification assistant.'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            
            content = response['message']['content'].strip()
            
            # Clean markdown code blocks if present
            if content.startswith('```'):
                lines = content.split('\n')
                content_lines = []
                for line in lines:
                    if not line.startswith('```'):
                        content_lines.append(line)
                content = '\n'.join(content_lines).strip()
            
            data = json.loads(content)
            
            # Ensure required keys exist and normalise emotion
            emotion = data.get('emotion', 'neutral').lower()
            if emotion not in ['joy', 'sadness', 'anger', 'fear', 'neutral']:
                emotion = 'neutral'
                
            confidence = data.get('confidence', 0.5)
            scores = data.get('scores', {})
            
            # Import UI mappings
            from nlp.myanmar_emotion_detector import EMOTION_EMOJIS, EMOTION_COLORS
            
            return {
                'emotion': emotion,
                'confidence': round(confidence, 3),
                'emoji': EMOTION_EMOJIS.get(emotion, '😐'),
                'color': EMOTION_COLORS.get(emotion, 'gray'),
                'scores': scores,
                'language': language,
                'method': 'myanmar_llm' if language == 'my' else 'english_llm',
            }
            
        except Exception as e:
            print(f"Ollama detect_emotion error: {e}")
            return None

    
    def _build_prompt(self, emotion: str, context: str) -> str:
        """Build prompt for LLM"""
        return f"""
User is feeling: {emotion.upper()}
Context: "{context}"

Provide 2-3 diverse recommendations in this JSON format:
{{
    "recommendations": [
        {{
            "type": "action",
            "label": "Mindfulness",
            "text": "calming exercise"
        }},
        {{
            "type": "action",
            "label": "Daily Exercise",
            "text": "active physical/mental task to soothe or celebrate the emotion"
        }}
    ]
}}

Only respond with valid JSON, no additional text. Do NOT include any general 'Activity' or 'Self-care' recommendations.
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
                # Filter out any Self-care or Activity recommendations
                recs = [
                    r for r in data['recommendations'] 
                    if r.get('label') not in ('Self-care', 'Self-Care Action', 'Activity', 'Activity Action')
                ]
                return {
                    'recommendations': recs,
                    'count': len(recs)
                }
            
            # Fallback to old format (2 recommendations)
            if 'send_message' in data and 'action' in data:
                return {
                    'recommendations': [
                        {'type': 'action', 'label': 'Self-Care Action', 'text': data['action']}
                    ],
                    'count': 1
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


def detect_emotion_ai(text: str, language: str = 'my') -> Optional[Dict]:
    """
    Convenience function to detect emotion using Ollama LLM
    """
    try:
        return get_agent().detect_emotion(text, language)
    except Exception:
        return None



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
                print(f"  recommendations: {rec['recommendations']}")
            else:
                print("  (AI failed, would use fallback)")
