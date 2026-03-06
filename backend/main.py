"""
Emotion-Aware Bot - FastAPI Backend
Main server with endpoints for emotion detection and recommendations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

# Import modules
from nlp.emotion_detector import detect_emotion
from ai.groq_agent import get_ai_recommendations, get_agent
from ai.fallback_rules import get_recommendations as get_rule_recommendations
from speech.stt import transcribe_speech

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Emotion-Aware Bot API",
    description="Detect emotions from text/speech and provide AI-powered recommendations",
    version="1.0.0"
)

# CORS middleware (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class TextAnalysisRequest(BaseModel):
    text: str
    use_ai: Optional[bool] = True


class VoiceAnalysisRequest(BaseModel):
    audio_base64: str
    use_ai: Optional[bool] = True


class AnalysisResponse(BaseModel):
    text: str
    emotion: str
    confidence: float
    emoji: str
    color: str
    recommendations: list  # Changed to list for multiple recommendations
    source: str  # "ai" or "rules"
    count: int  # Number of recommendations
    scores: Optional[Dict[str, float]] = None


class HealthResponse(BaseModel):
    status: str
    ai_available: bool
    message: str


# Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Emotion-Aware Bot API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/api/detect/text",
            "/api/detect/voice"
        ]
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and AI availability"""
    ai_available = get_agent().is_available()
    
    return {
        "status": "ok",
        "ai_available": ai_available,
        "message": "AI recommendations enabled" if ai_available else "Using rule-based recommendations"
    }


@app.post("/api/detect/text", response_model=AnalysisResponse, tags=["Analysis"])
async def detect_from_text(request: TextAnalysisRequest):
    """
    Detect emotion from text and get recommendations
    
    Args:
        request: TextAnalysisRequest with text and use_ai flag
        
    Returns:
        AnalysisResponse with emotion, confidence, and recommendations
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # 1. Detect emotion using NLTK
    emotion_result = detect_emotion(request.text)
    
    # 2. Get recommendations (AI or Rules)
    recommendations_result = {}
    source = "rules"
    rec_count = 0

    if request.use_ai:
        # Try AI first
        ai_recs = get_ai_recommendations(
            emotion_result['emotion'],
            request.text
        )

        if ai_recs and 'recommendations' in ai_recs:
            recommendations_result = ai_recs['recommendations']
            rec_count = ai_recs.get('count', len(ai_recs['recommendations']))
            source = "ai"
        else:
            # Fallback to rules
            rule_recs = get_rule_recommendations(emotion_result['emotion'])
            recommendations_result = rule_recs.get('recommendations', [])
            rec_count = rule_recs.get('count', len(rule_recs['recommendations']))
            source = "rules"
    else:
        # Use rules only
        rule_recs = get_rule_recommendations(emotion_result['emotion'])
        recommendations_result = rule_recs.get('recommendations', [])
        rec_count = rule_recs.get('count', len(rule_recs['recommendations']))

    # 3. Build response
    return {
        "text": request.text,
        "emotion": emotion_result['emotion'],
        "confidence": emotion_result['confidence'],
        "emoji": emotion_result['emoji'],
        "color": emotion_result['color'],
        "recommendations": recommendations_result,
        "count": rec_count,
        "source": source,
        "scores": emotion_result['scores']
    }


@app.post("/api/detect/voice", response_model=AnalysisResponse, tags=["Analysis"])
async def detect_from_voice(request: VoiceAnalysisRequest):
    """
    Detect emotion from voice audio and get recommendations
    
    Args:
        request: VoiceAnalysisRequest with base64-encoded audio
        
    Returns:
        AnalysisResponse with transcribed text, emotion, and recommendations
    """
    if not request.audio_base64.strip():
        raise HTTPException(status_code=400, detail="Audio cannot be empty")
    
    # 1. Transcribe speech to text
    try:
        transcribed_text = transcribe_speech(
            audio_data=None,  # Will use base64 internally
            from_mic=False
        )
        
        # Use the base64 method directly
        from speech.stt import get_stt
        transcribed_text = get_stt().transcribe_from_base64(request.audio_base64)
        
        if not transcribed_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    
    # 2. Detect emotion using NLTK
    emotion_result = detect_emotion(transcribed_text)
    
    # 3. Get recommendations (AI or Rules)
    recommendations_result = []
    source = "rules"
    rec_count = 0

    if request.use_ai:
        # Try AI first
        ai_recs = get_ai_recommendations(
            emotion_result['emotion'],
            transcribed_text
        )

        if ai_recs and 'recommendations' in ai_recs:
            recommendations_result = ai_recs['recommendations']
            rec_count = ai_recs.get('count', len(ai_recs['recommendations']))
            source = "ai"
        else:
            # Fallback to rules
            rule_recs = get_rule_recommendations(emotion_result['emotion'])
            recommendations_result = rule_recs.get('recommendations', [])
            rec_count = rule_recs.get('count', len(rule_recs['recommendations']))
            source = "rules"
    else:
        # Use rules only
        rule_recs = get_rule_recommendations(emotion_result['emotion'])
        recommendations_result = rule_recs.get('recommendations', [])
        rec_count = rule_recs.get('count', len(rule_recs['recommendations']))

    # 4. Build response
    return {
        "text": transcribed_text,
        "emotion": emotion_result['emotion'],
        "confidence": emotion_result['confidence'],
        "emoji": emotion_result['emoji'],
        "color": emotion_result['color'],
        "recommendations": recommendations_result,
        "count": rec_count,
        "source": source,
        "scores": emotion_result['scores']
    }


# Run server
if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║       🧠 Emotion-Aware Bot API Server                    ║
    ╠══════════════════════════════════════════════════════════╣
    ║  Starting server on http://{host}:{port}                    ║
    ║  API Docs: http://{host}:{port}/docs                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host=host, port=port)
