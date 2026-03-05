"""
Speech-to-Text Module using SpeechRecognition
Converts voice audio to text for emotion analysis
"""

import speech_recognition as sr
from typing import Optional, Dict
import base64
import io


class SpeechToText:
    """Convert speech to text using Google Speech API"""
    
    def __init__(self):
        """Initialize speech recognizer"""
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
    
    def transcribe_from_microphone(self, timeout: int = 5) -> Optional[str]:
        """
        Transcribe speech from microphone
        
        Args:
            timeout: Seconds to wait for speech
            
        Returns:
            Transcribed text or None
        """
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout)
                
                # Recognize speech using Google Web Speech API
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"API error: {e}")
            return None
        except Exception as e:
            print(f"Microphone error: {e}")
            return None
    
    def transcribe_from_audio_data(self, audio_data: bytes, sample_rate: int = 16000) -> Optional[str]:
        """
        Transcribe from raw audio data
        
        Args:
            audio_data: Raw audio bytes (WAV format)
            sample_rate: Audio sample rate (default 16000)
            
        Returns:
            Transcribed text or None
        """
        try:
            # Create AudioData object
            audio = sr.AudioData(audio_data, sample_rate, 2)  # 2 = sample_width (16-bit)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"API error: {e}")
            return None
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
    
    def transcribe_from_file(self, file_path: str) -> Optional[str]:
        """
        Transcribe from audio file
        
        Args:
            file_path: Path to WAV file
            
        Returns:
            Transcribed text or None
        """
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
                
        except Exception as e:
            print(f"File transcription error: {e}")
            return None
    
    def transcribe_from_base64(self, audio_base64: str) -> Optional[str]:
        """
        Transcribe from base64-encoded audio
        
        Args:
            audio_base64: Base64-encoded audio data
            
        Returns:
            Transcribed text or None
        """
        try:
            # Decode base64
            audio_bytes = base64.b64decode(audio_base64)
            return self.transcribe_from_audio_data(audio_bytes)
            
        except Exception as e:
            print(f"Base64 decoding error: {e}")
            return None


# Singleton instance
_stt = None


def get_stt() -> SpeechToText:
    """Get or create SpeechToText singleton"""
    global _stt
    if _stt is None:
        _stt = SpeechToText()
    return _stt


def transcribe_speech(audio_data: bytes = None, from_mic: bool = False) -> Optional[str]:
    """
    Convenience function to transcribe speech
    
    Args:
        audio_data: Raw audio bytes (if not from mic)
        from_mic: If True, listen from microphone
        
    Returns:
        Transcribed text or None
    """
    stt = get_stt()
    
    if from_mic:
        return stt.transcribe_from_microphone()
    elif audio_data:
        return stt.transcribe_from_audio_data(audio_data)
    else:
        return None


if __name__ == "__main__":
    # Test microphone transcription
    print("Testing microphone...")
    stt = SpeechToText()
    text = stt.transcribe_from_microphone()
    if text:
        print(f"Transcribed: {text}")
    else:
        print("Failed to transcribe")
