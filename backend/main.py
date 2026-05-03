"""
Emotion-Aware Bot - FastAPI Backend
Main server with endpoints for emotion detection and recommendations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import os
from dotenv import load_dotenv

# Import modules
from nlp.emotion_detector import detect_emotion
from nlp.hmm_classifier import get_classifier as get_hmm_classifier
from ai.groq_agent import get_ai_recommendations, get_agent
from ai.fallback_rules import get_recommendations as get_rule_recommendations
from ai.multi_source_recommender import get_recommendations as get_multi_source_recommendations
from ai.external_resource_recommender import get_external_recommendations
from nlp.myanmar_emotion_detector import is_myanmar_text, EMOTION_EMOJIS, EMOTION_COLORS
from ai.face_emotion_detector import analyze_face_emotion
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
    use_ai: bool = False
    method: str = "vader"  # "vader", "hmm", "hybrid"

class ImageAnalysisRequest(BaseModel):
    image: str  # Base64 encoded image
    language: str = "en"


class VoiceAnalysisRequest(BaseModel):
    audio_base64: str
    use_ai: Optional[bool] = True
    method: Optional[str] = "vader"


class AnalysisResponse(BaseModel):
    text: str
    emotion: str
    confidence: float
    emoji: str
    color: str
    recommendations: Any  # Can be dict (multi-source) or list (dev branch)
    source: str  # "ai" or "rules"
    count: Optional[int] = None  # Number of recommendations (dev branch)
    scores: Optional[Dict[str, float]] = None
    method: Optional[str] = "vader"
    language: Optional[str] = "en"  # "en" for English, "my" for Myanmar
    multi_source: Optional[Dict[str, Any]] = None  # Multi-source recommendations
    external_resources: Optional[Dict[str, Any]] = None  # External API recommendations


class HealthResponse(BaseModel):
    status: str
    ai_available: bool
    hmm_available: bool
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
    
    # Check HMM model availability
    hmm_available = False
    try:
        hmm_classifier = get_hmm_classifier()
        hmm_available = hmm_classifier.is_trained
    except Exception:
        hmm_available = False

    return {
        "status": "ok",
        "ai_available": ai_available,
        "hmm_available": hmm_available,
        "message": "AI recommendations enabled" if ai_available else "Using rule-based recommendations"
    }


@app.post("/api/detect/text", response_model=AnalysisResponse, tags=["Analysis"])
async def detect_from_text(request: TextAnalysisRequest):
    """
    Detect emotion from text and get recommendations

    Args:
        request: TextAnalysisRequest with text, use_ai flag, and method

    Returns:
        AnalysisResponse with emotion, confidence, and recommendations
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # 1. Detect emotion using specified method
    method = request.method.lower()

    # PRIORITIZE MYANMAR LANGUAGE
    from nlp.myanmar_emotion_detector import is_myanmar_text
    
    if is_myanmar_text(request.text):
        emotion_result = detect_emotion(request.text)
        emotion_result['method'] = 'myanmar_keyword'
        method = 'myanmar_keyword'
    elif method == "hmm":
        # Use HMM classifier for English
        try:
            hmm_classifier = get_hmm_classifier()
            if not hmm_classifier.is_trained:
                # Fallback to VADER if HMM not trained
                emotion_result = detect_emotion(request.text)
                emotion_result['method'] = 'vader'
                method = 'vader'
            else:
                emotion_result = hmm_classifier.detect(request.text)
                emotion_result['method'] = 'hmm'
        except Exception:
            emotion_result = detect_emotion(request.text)
            emotion_result['method'] = 'vader'
            method = 'vader'
    elif method == "hybrid":
        # Use both VADER and HMM for English, combine results
        vader_result = detect_emotion(request.text)
        try:
            hmm_classifier = get_hmm_classifier()
            if hmm_classifier.is_trained:
                hmm_result = hmm_classifier.detect(request.text)
                # If both agree, increase confidence
                if vader_result['emotion'] == hmm_result['emotion']:
                    vader_result['confidence'] = min(1.0, vader_result['confidence'] + 0.1)
                else:
                    # Use VADER but note disagreement
                    vader_result['hmm_emotion'] = hmm_result['emotion']
                    vader_result['hmm_confidence'] = hmm_result['confidence']
        except Exception:
            pass
        emotion_result = vader_result
        emotion_result['method'] = 'hybrid'
        method = 'hybrid'
    else:
        # Default to VADER for English
        emotion_result = detect_emotion(request.text)
        emotion_result['method'] = 'vader'
        method = 'vader'

    # 2. Get recommendations (AI or Rules)
    recommendations_result: Any = {}
    source = "rules"
    rec_count = 0

    if request.use_ai:
        # Try AI first
        ai_recs = get_ai_recommendations(
            emotion_result['emotion'],
            request.text
        )

        if ai_recs and 'recommendations' in ai_recs:
            # Dev branch format (list-based)
            recommendations_result = ai_recs['recommendations']
            rec_count = ai_recs.get('count', len(ai_recs['recommendations']))
            source = "ai"
        elif ai_recs:
            # Our format (dict-based)
            recommendations_result = ai_recs
            source = "ai"
        else:
            # Fallback to rules
            rule_recs = get_rule_recommendations(emotion_result['emotion'], request.text)
            if isinstance(rule_recs, list):
                # Dev branch format
                recommendations_result = rule_recs
                rec_count = len(rule_recs)
            else:
                # Our format (multi-source dict)
                recommendations_result = rule_recs
                rec_count = 1
            source = "rules"
    else:
        # Use rules only
        rule_recs = get_rule_recommendations(emotion_result['emotion'], request.text)
        if isinstance(rule_recs, list):
            recommendations_result = rule_recs
            rec_count = len(rule_recs)
        else:
            recommendations_result = rule_recs
            rec_count = 1

    # Detect language from emotion result
    detected_language = emotion_result.get('language', 'en')

    # Get multi-source recommendations
    multi_source_recs = get_multi_source_recommendations(
        emotion=emotion_result['emotion'],
        context=request.text,
        source_types=['music', 'podcast', 'video', 'activity', 'self_care'],
        language=detected_language
    )

    # Get external resource recommendations (YouTube, Spotify, etc.)
    external_recs = get_external_recommendations(
        emotion=emotion_result['emotion'],
        context=request.text,
        sources=['youtube', 'spotify', 'podcast', 'ted']
    )

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
        "scores": emotion_result.get('scores'),
        "method": method,
        "language": detected_language,
        "multi_source": multi_source_recs,
        "external_resources": external_recs
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
        from speech.stt import get_stt
        transcribed_text = get_stt().transcribe_from_base64(request.audio_base64)

        if not transcribed_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    # 2. Detect emotion using specified method
    method = request.method.lower() if hasattr(request, 'method') else "vader"
    
    # PRIORITIZE MYANMAR LANGUAGE
    from nlp.myanmar_emotion_detector import is_myanmar_text
    if is_myanmar_text(transcribed_text):
        emotion_result = detect_emotion(transcribed_text)
        emotion_result['method'] = 'myanmar_keyword'
        method = 'myanmar_keyword'
    elif method == "hmm":
        try:
            hmm_classifier = get_hmm_classifier()
            if not hmm_classifier.is_trained:
                emotion_result = detect_emotion(transcribed_text)
                emotion_result['method'] = 'vader'
                method = 'vader'
            else:
                emotion_result = hmm_classifier.detect(transcribed_text)
                emotion_result['method'] = 'hmm'
        except Exception:
            emotion_result = detect_emotion(transcribed_text)
            emotion_result['method'] = 'vader'
            method = 'vader'
    elif method == "hybrid":
        # Use both VADER and HMM for English
        vader_result = detect_emotion(transcribed_text)
        try:
            hmm_classifier = get_hmm_classifier()
            if hmm_classifier.is_trained:
                hmm_result = hmm_classifier.detect(transcribed_text)
                # If both agree, increase confidence
                if vader_result['emotion'] == hmm_result['emotion']:
                    vader_result['confidence'] = min(1.0, vader_result['confidence'] + 0.1)
                else:
                    vader_result['hmm_emotion'] = hmm_result['emotion']
                    vader_result['hmm_confidence'] = hmm_result['confidence']
        except Exception:
            pass
        emotion_result = vader_result
        emotion_result['method'] = 'hybrid'
        method = 'hybrid'
    else:
        # Default to VADER for English
        emotion_result = detect_emotion(transcribed_text)
        emotion_result['method'] = 'vader'
        method = 'vader'

    # 3. Get recommendations (AI or Rules)
    recommendations_result: Any = {}
    source = "rules"
    rec_count = 0

    # Detect language from emotion result
    detected_language = emotion_result.get('language', 'en')

    if request.use_ai:
        # Try AI first
        ai_recs = get_ai_recommendations(
            emotion_result['emotion'],
            transcribed_text,
            language=detected_language
        )

        if ai_recs and 'recommendations' in ai_recs:
            recommendations_result = ai_recs['recommendations']
            rec_count = len(recommendations_result)
            source = "ai"
        elif ai_recs:
            recommendations_result = ai_recs
            source = "ai"
        else:
            rule_recs = get_rule_recommendations(emotion_result['emotion'], transcribed_text)
            recommendations_result = rule_recs if isinstance(rule_recs, list) else [rule_recs]
            rec_count = len(recommendations_result)
            source = "rules"
    else:
        rule_recs = get_rule_recommendations(emotion_result['emotion'], transcribed_text)
        recommendations_result = rule_recs if isinstance(rule_recs, list) else [rule_recs]
        rec_count = len(recommendations_result)
        source = "rules"

    # Detect language from emotion result
    detected_language = emotion_result.get('language', 'en')

    # Get multi-source recommendations
    multi_source_recs = get_multi_source_recommendations(
        emotion=emotion_result['emotion'],
        context=transcribed_text,
        source_types=['music', 'podcast', 'video', 'activity', 'social', 'self_care'],
        language=detected_language
    )

    # Get external resource recommendations
    external_recs = get_external_recommendations(
        emotion=emotion_result['emotion'],
        context=transcribed_text,
        sources=['youtube', 'spotify', 'podcast', 'ted']
    )

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
        "scores": emotion_result.get('scores'),
        "method": method,
        "language": detected_language,
        "multi_source": multi_source_recs,
        "external_resources": external_recs
    }


# Run server
@app.post("/api/detect/image", response_model=AnalysisResponse)
async def detect_from_image(request: ImageAnalysisRequest):
    """
    Detect emotion from a captured face image
    """
    # 1. Analyze face emotion
    result = analyze_face_emotion(request.image)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    emotion = result["emotion"]
    confidence = result["confidence"]
    
    # 2. Get recommendations based on detected emotion and language
    multi_source_recs = get_multi_source_recommendations(
        emotion=emotion,
        source_types=['music', 'podcast', 'video', 'activity', 'self_care'],
        language=request.language
    )
    
    # Get external resource recommendations
    external_recs = get_external_recommendations(
        emotion=emotion,
        sources=['youtube', 'spotify', 'podcast', 'ted']
    )
    
    # 3. Hybrid Approach: Add AI-generated recommendations (Method 3)
    from nlp.myanmar_emotion_detector import EMOTION_EMOJIS, EMOTION_COLORS
    
    # Generate natural text response
    if request.language == 'my':
        my_emotions = {
            'joy': 'ပျော်ရွှင်',
            'sadness': 'ဝမ်းနည်း',
            'anger': 'ဒေါသထွက်',
            'fear': 'ကြောက်ရွံ့',
            'neutral': 'ပုံမှန်'
        }
        emo_name = my_emotions.get(emotion, 'ပုံမှန်')
        display_text = f"သင့်မျက်နှာအမူအရာအရ {emo_name}နေတဲ့ ခံစားချက်ကို တွေ့ရှိရပါတယ်ဗျ။"
    else:
        display_text = f"I detected {emotion} in your facial expression."

    from ai.groq_agent import get_ai_recommendations
    ai_recs = get_ai_recommendations(
        emotion=emotion,
        context=display_text,
        language=request.language
    )
    
    recommendations_result = []
    source = "rules"
    if ai_recs and 'recommendations' in ai_recs:
        recommendations_result = ai_recs['recommendations']
        source = "ai"

    return {
        "text": display_text,
        "emotion": emotion,
        "confidence": confidence,
        "emoji": EMOTION_EMOJIS.get(emotion, "😐"),
        "color": EMOTION_COLORS.get(emotion, "gray"),
        "recommendations": recommendations_result, # AI recommendations
        "multi_source": multi_source_recs, # Manual Core
        "external_resources": external_recs, # External
        "source": source,
        "method": "facial_recognition",
        "language": request.language
    }

class SocialAnalysisRequest(BaseModel):
    message: str
    perspective: str = "receiver"  # "receiver" or "sender"
    language: str = "en"

@app.post("/api/social/analyze")
async def analyze_social_message(request: SocialAnalysisRequest):
    """
    Analyze a social message (relationship advice)
    """
    from ai.groq_agent import get_social_advice
    
    advice = get_social_advice(
        request.message, 
        request.perspective, 
        request.language
    )
    
    if not advice:
        raise HTTPException(status_code=500, detail="Failed to get social advice")
        
    return advice

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║       🧠 Emotion-Aware Bot API Server                    ║
    ╠══════════════════════════════════════════════════════════╣
    ║  Starting server on http://{host}:{port}                 ║
    ║  API Docs: http://{host}:{port}/docs                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(app, host=host, port=port)
