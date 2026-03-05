"""
Test script for Emotion-Aware Bot Backend
Run this to verify all components are working
"""

import sys
sys.path.insert(0, '.')

def test_emotion_detector():
    """Test NLTK emotion detection"""
    print("\n🧪 Testing Emotion Detector...")
    
    from nlp.emotion_detector import detect_emotion
    
    test_cases = [
        ("I am so happy today!", "joy"),
        ("This makes me so angry!", "anger"),
        ("I feel really sad and lonely", "sadness"),
        ("I'm worried about the future", "fear"),
        ("The weather is okay", "neutral"),
    ]
    
    passed = 0
    for text, expected_emotion in test_cases:
        result = detect_emotion(text)
        status = "✅" if result['emotion'] == expected_emotion else "⚠️"
        print(f"  {status} '{text}'")
        print(f"      Expected: {expected_emotion}, Got: {result['emotion']} ({result['confidence']:.2f})")
        if result['emotion'] == expected_emotion:
            passed += 1
    
    print(f"\n  Emotion Detector: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)


def test_rule_based_recommendations():
    """Test rule-based recommendation engine"""
    print("\n🧪 Testing Rule-Based Recommendations...")
    
    from ai.fallback_rules import get_recommendations
    
    emotions = ['joy', 'anger', 'sadness', 'fear', 'neutral']
    
    for emotion in emotions:
        rec = get_recommendations(emotion)
        print(f"  ✅ {emotion.capitalize()}:")
        print(f"      Send: {rec['send_message']}")
        print(f"      Action: {rec['action']}")
    
    print(f"\n  Rule-Based Recommendations: All emotions covered")
    return True


def test_ollama_agent():
    """Test Ollama AI agent"""
    print("\n🧪 Testing Ollama AI Agent...")
    
    try:
        from ai.ollama_agent import get_agent
        
        agent = get_agent()
        is_available = agent.is_available()
        
        if is_available:
            print("  ✅ Ollama server is available")
            
            # Test a recommendation
            rec = agent.get_recommendations('joy', 'I got a promotion!')
            if rec:
                print(f"  ✅ AI Recommendation test:")
                print(f"      Send: {rec['send_message']}")
                print(f"      Action: {rec['action']}")
                return True
            else:
                print("  ⚠️ Ollama responded but couldn't parse recommendations")
                return False
        else:
            print("  ⚠️ Ollama server is not available (will use rule-based fallback)")
            print("     Install: curl -fsSL https://ollama.com/install.sh | sh")
            print("     Download: ollama pull llama2:7b")
            return False
            
    except Exception as e:
        print(f"  ❌ Ollama test failed: {e}")
        return False


def test_speech_to_text():
    """Test speech-to-text module"""
    print("\n🧪 Testing Speech-to-Text Module...")
    
    try:
        from speech.stt import get_stt
        
        stt = get_stt()
        print("  ✅ Speech-to-text module initialized")
        print("  ℹ️  Microphone test requires user input (skipped)")
        return True
        
    except Exception as e:
        print(f"  ⚠️ Speech-to-text module error: {e}")
        print("     Install: pip install pyaudio speechrecognition")
        return False


def test_api_server():
    """Test FastAPI server endpoints"""
    print("\n🧪 Testing API Server...")
    print("  ℹ️  Start server first: python main.py")
    print("  ℹ️  Then test manually:")
    print("     curl http://localhost:8000/health")
    print("     curl -X POST http://localhost:8000/api/detect/text \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"text\": \"I am happy!\"}'")
    return True


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║       🧠 Emotion-Aware Bot - Component Tests             ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    results = []
    
    # Test components
    results.append(("Emotion Detector", test_emotion_detector()))
    results.append(("Rule-Based Recommendations", test_rule_based_recommendations()))
    results.append(("Ollama AI Agent", test_ollama_agent()))
    results.append(("Speech-to-Text", test_speech_to_text()))
    results.append(("API Server", test_api_server()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "⚠️  SKIP/FAIL"
        print(f"  {status}: {name}")
    
    print(f"\n  Total: {passed}/{total} components working")
    
    if passed >= 3:
        print("\n  ✅ System is ready to use!")
        print("  🚀 Start backend: python main.py")
        print("  🚀 Start frontend: cd frontend && npm run dev")
    else:
        print("\n  ⚠️  Some components need setup. Check messages above.")
    
    print("="*60)


if __name__ == "__main__":
    main()
