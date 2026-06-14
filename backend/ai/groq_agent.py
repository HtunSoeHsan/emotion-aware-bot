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
    SYSTEM_PROMPT = """You are an empathetic emotional support assistant. 
Your task is to provide helpful, actionable recommendations for someone experiencing an emotion.

For each request, provide 2-3 diverse recommendations focusing solely on:
1. Mindfulness: Short calming exercises or breathing techniques.
2. Daily Exercise: Active physical or mental tasks to soothe or celebrate the emotion.

Do NOT include any general activities, activity cards, self-care tips/advice, social replies, relationship advice, or messages to send to others.
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
                max_tokens=800,
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

    def detect_emotion(self, text: str, language: str = 'my') -> Optional[Dict]:
        """
        Classify emotion of text using Groq LLM
        
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a precise emotion classification assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # low temperature for classification stability
                max_tokens=150,
                timeout=10
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean markdown code blocks if present
            if content.startswith('```'):
                lines = content.split('\n')
                # Find start and end of json
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
            print(f"Groq detect_emotion error: {e}")
            return None

    
    def _build_prompt(self, emotion: str, context: str, language: str = 'en') -> str:
        """Build prompt for LLM"""
        lang_instruction = "IMPORTANT: Provide all text in Myanmar (Burmese) language." if language == 'my' else "Provide all text in English."
        
        return f"""
User is feeling: {emotion.upper()}
Context/Message: "{context}"

{lang_instruction}

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
                        {'type': 'message', 'label': 'Send Message', 'text': data['send_message']},
                        {'type': 'action', 'label': 'Self-Care Action', 'text': data['action']}
                    ],
                    'count': 2
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


def detect_emotion_ai(text: str, language: str = 'my') -> Optional[Dict]:
    """
    Convenience function to detect emotion using Groq LLM
    """
    try:
        return get_agent().detect_emotion(text, language)
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
                    print(f"  ✅ recommendations: {rec['recommendations']}")
                else:
                    print("  ❌ (Failed to get recommendations)")
                    
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("   Please set GROQ_API_KEY in .env file")
    except Exception as e:
        print(f"❌ Error: {e}")
