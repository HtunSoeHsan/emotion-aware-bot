"""
Test script for HMM-based Emotion Classifier
Compares HMM predictions with VADER results
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from nlp.hmm_classifier import HMMEmotionClassifier, load_hmm_classifier
from nlp.emotion_detector import detect_emotion
import os


def test_hmm_classifier():
    """Test HMM classifier with sample data"""
    
    print("=" * 70)
    print("HMM Emotion Classifier - Test Suite")
    print("=" * 70)
    
    # Check if trained model exists
    model_path = backend_dir / "nlp" / "models" / "hmm_emotion_model.pkl"
    
    if os.path.exists(model_path):
        print(f"\n✓ Loading trained model from {model_path}")
        classifier = load_hmm_classifier(str(model_path))
    else:
        print(f"\n✗ No trained model found at {model_path}")
        print("  Please run: python backend/nlp/train_hmm.py")
        print("\n  Running quick training for demonstration...")
        
        # Quick training with minimal data
        training_data = {
            'joy': [
                "I am so happy today!",
                "This is wonderful news!",
                "I love this so much!",
                "Feeling great and excited!",
                "Best day ever, so joyful!",
                "I'm thrilled and delighted!",
                "What a happy moment!",
                "Feeling amazing and cheerful!"
            ],
            'anger': [
                "This makes me so angry!",
                "I'm furious about this!",
                "That's really annoying!",
                "I hate this situation!",
                "So frustrated and mad!",
                "This is outrageous!",
                "I'm irritated and upset!",
                "Absolutely infuriating!"
            ],
            'sadness': [
                "I feel really sad and lonely",
                "This is so depressing",
                "I'm feeling down today",
                "Heartbroken and miserable",
                "So sad and disappointed",
                "Feeling blue and tearful",
                "Everything feels hopeless",
                "Crying and feeling low"
            ],
            'fear': [
                "I'm worried about the future",
                "This is scary and frightening",
                "I'm anxious and nervous",
                "Feeling terrified and panicked",
                "So afraid and worried",
                "This makes me nervous",
                "I'm scared of what might happen",
                "Feeling anxious and fearful"
            ],
            'neutral': [
                "The weather is okay",
                "Just another regular day",
                "Nothing special happening",
                "Feeling normal today",
                "It's an average day",
                "Everything is fine",
                "No strong feelings",
                "Just feeling normal"
            ]
        }
        
        classifier = HMMEmotionClassifier(n_components=3, n_features=50)
        classifier.train(training_data, n_iterations=50)
    
    # Test cases
    test_cases = [
        ("I am so happy today!", "joy"),
        ("This makes me so angry!", "anger"),
        ("I feel really sad and lonely", "sadness"),
        ("I'm worried about the future", "fear"),
        ("The weather is okay", "neutral"),
        ("I'm absolutely thrilled and excited!", "joy"),
        ("This is so frustrating and annoying!", "anger"),
        ("I feel so alone and depressed", "sadness"),
        ("I'm terrified and scared", "fear"),
        ("It's just a normal day", "neutral")
    ]
    
    print("\n" + "-" * 70)
    print("Test Results:")
    print("-" * 70)
    
    hmm_correct = 0
    vader_correct = 0
    
    results = []
    
    for text, expected in test_cases:
        # HMM prediction
        hmm_result = classifier.detect(text)
        hmm_predicted = hmm_result['emotion']
        hmm_confidence = hmm_result['confidence']
        
        # VADER prediction
        vader_result = detect_emotion(text)
        vader_predicted = vader_result['emotion']
        vader_confidence = vader_result['confidence']
        
        # Check accuracy
        hmm_match = hmm_predicted == expected
        vader_match = vader_predicted == expected
        
        if hmm_match:
            hmm_correct += 1
        if vader_match:
            vader_correct += 1
        
        results.append({
            'text': text,
            'expected': expected,
            'hmm_predicted': hmm_predicted,
            'hmm_confidence': hmm_confidence,
            'vader_predicted': vader_predicted,
            'vader_confidence': vader_confidence,
            'hmm_match': hmm_match,
            'vader_match': vader_match
        })
    
    # Print detailed results
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Text: \"{result['text']}\"")
        print(f"   Expected: {result['expected']}")
        
        hmm_symbol = "✓" if result['hmm_match'] else "✗"
        vader_symbol = "✓" if result['vader_match'] else "✗"
        
        print(f"   HMM:    {hmm_symbol} {result['hmm_predicted']} (confidence: {result['hmm_confidence']:.3f})")
        print(f"   VADER:  {vader_symbol} {result['vader_predicted']} (confidence: {result['vader_confidence']:.3f})")
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    print(f"Total test cases: {len(test_cases)}")
    print(f"HMM Accuracy:   {hmm_correct}/{len(test_cases)} ({hmm_correct/len(test_cases)*100:.1f}%)")
    print(f"VADER Accuracy: {vader_correct}/{len(test_cases)} ({vader_correct/len(test_cases)*100:.1f}%)")
    print("=" * 70)
    
    # Additional test: Show all emotion scores for one example
    print("\n" + "-" * 70)
    print("Detailed Score Breakdown (Example):")
    print("-" * 70)
    
    example_text = "I am so happy today!"
    hmm_result = classifier.detect(example_text)
    vader_result = detect_emotion(example_text)
    
    print(f"\nText: \"{example_text}\"\n")
    
    print("HMM Scores:")
    for emotion, score in hmm_result['scores'].items():
        bar = "█" * int(score * 20)
        print(f"  {emotion:10s}: {score:.3f} {bar}")
    
    print("\nVADER Scores:")
    for emotion, score in vader_result['scores'].items():
        bar = "█" * int(score * 20)
        print(f"  {emotion:10s}: {score:.3f} {bar}")
    
    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)
    
    return hmm_correct, vader_correct


def compare_performance():
    """Compare HMM vs VADER performance"""
    
    print("\n\n")
    print("=" * 70)
    print("Performance Comparison: HMM vs VADER")
    print("=" * 70)
    
    # Test with varying text lengths
    test_sets = {
        'Short (3-5 words)': [
            "I am so happy!",
            "This makes me mad!",
            "I feel sad today",
            "I'm really scared",
            "It is okay"
        ],
        'Medium (6-10 words)': [
            "I am so happy with this result!",
            "This situation makes me really angry!",
            "I feel so sad and lonely today",
            "I'm worried about what might happen",
            "Everything is just fine and normal"
        ],
        'Long (11+ words)': [
            "I am so incredibly happy and excited about this wonderful news!",
            "This situation makes me so angry and frustrated I could scream!",
            "I feel really sad and depressed about everything that happened today!",
            "I'm so worried and anxious about all the things that could go wrong!",
            "Everything is just fine and I'm feeling completely normal today!"
        ]
    }
    
    for length_type, texts in test_sets.items():
        print(f"\n{length_type}:")
        print("-" * 40)
        
        hmm_correct = 0
        vader_correct = 0
        
        for text in texts:
            # Determine expected emotion from keywords
            if 'happy' in text.lower() or 'excited' in text.lower():
                expected = 'joy'
            elif 'angry' in text.lower() or 'mad' in text.lower() or 'frustrated' in text.lower():
                expected = 'anger'
            elif 'sad' in text.lower() or 'depressed' in text.lower() or 'lonely' in text.lower():
                expected = 'sadness'
            elif 'worried' in text.lower() or 'scared' in text.lower() or 'anxious' in text.lower():
                expected = 'fear'
            else:
                expected = 'neutral'
            
            hmm_result = classifier.detect(text)
            vader_result = detect_emotion(text)
            
            if hmm_result['emotion'] == expected:
                hmm_correct += 1
            if vader_result['emotion'] == expected:
                vader_correct += 1
        
        print(f"  HMM:    {hmm_correct}/{len(texts)} ({hmm_correct/len(texts)*100:.0f}%)")
        print(f"  VADER:  {vader_correct}/{len(texts)} ({vader_correct/len(texts)*100:.0f}%)")


if __name__ == "__main__":
    # Run tests
    hmm_correct, vader_correct = test_hmm_classifier()
    
    # Ask if user wants to run performance comparison
    print("\n")
    try:
        choice = input("Run performance comparison? (y/n): ").strip().lower()
        if choice == 'y':
            # Need to reload classifier for this
            model_path = backend_dir / "nlp" / "models" / "hmm_emotion_model.pkl"
            if os.path.exists(model_path):
                classifier = load_hmm_classifier(str(model_path))
                compare_performance()
            else:
                print("Please train the model first with: python backend/nlp/train_hmm.py")
    except Exception:
        pass
    
    print("\nDone!")
