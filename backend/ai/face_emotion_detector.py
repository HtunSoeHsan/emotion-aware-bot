import os
import base64
from typing import Dict, Any

def analyze_face_emotion(image_base64: str) -> Dict[Any, Any]:
    """
    Analyze emotion from a base64 encoded image string using DeepFace.
    """
    try:
        # Import inside function so server can start even if library is not yet installed
        import cv2
        import numpy as np
        from deepface import DeepFace
        
        # 1. Decode base64 image
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]
        
        img_data = base64.b64decode(image_base64)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {"error": "Invalid image data"}

        # 2. Use DeepFace to analyze emotion
        results = DeepFace.analyze(
            img_path=img, 
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv'
        )

        if not results:
            return {"error": "No face detected"}
            
        result = results[0]
        dominant_emotion = result['dominant_emotion']
        confidence = result['emotion'][dominant_emotion] / 100.0
        
        emotion_map = {
            'happy': 'joy',
            'sad': 'sadness',
            'angry': 'anger',
            'fear': 'fear',
            'neutral': 'neutral',
            'surprise': 'joy',
            'disgust': 'anger'
        }
        
        bot_emotion = emotion_map.get(dominant_emotion, 'neutral')
        
        return {
            "emotion": bot_emotion,
            "confidence": round(confidence, 3),
            "raw_emotion": dominant_emotion,
            "all_scores": result['emotion']
        }

    except ImportError:
        return {"error": "Facial recognition libraries are still installing. Please wait a few minutes."}
    except Exception as e:
        print(f"Face Analysis Error: {e}")
        return {"error": str(e)}
