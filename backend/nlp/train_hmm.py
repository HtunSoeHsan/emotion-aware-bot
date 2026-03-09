"""
Training script for HMM-based Emotion Classifier
Creates and saves a trained HMM model for emotion detection
"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from nlp.hmm_classifier import HMMEmotionClassifier, train_hmm_classifier


# Extended training dataset for better HMM performance
TRAINING_DATA = {
    'joy': [
        "I am so happy today!",
        "This is wonderful news!",
        "I love this so much!",
        "Feeling great and excited!",
        "Best day ever, so joyful!",
        "I'm thrilled and delighted!",
        "What a happy moment!",
        "Feeling amazing and cheerful!",
        "Overjoyed and ecstatic!",
        "This brings me so much joy!",
        "I'm feeling blessed and grateful!",
        "Absolutely fantastic experience!",
        "So pleased and satisfied!",
        "Feeling on top of the world!",
        "This is incredible and awesome!",
        "My heart is full of happiness!",
        "What a delightful surprise!",
        "Feeling radiant and brilliant!",
        "So much fun and enjoyment!",
        "I'm beaming with pride!",
        "Experiencing pure bliss!",
        "This makes my heart sing!",
        "Feeling wonderful and glorious!",
        "So excited and pumped!",
        "Living my best life!",
        "Feeling sunny and bright!",
        "This is so rewarding!",
        "I'm feeling uplifted!",
        "What a beautiful moment!",
        "Feeling festive and merry!"
    ],
    
    'anger': [
        "This makes me so angry!",
        "I'm furious about this!",
        "That's really annoying!",
        "I hate this situation!",
        "So frustrated and mad!",
        "This is outrageous!",
        "I'm irritated and upset!",
        "Absolutely infuriating!",
        "I'm boiling with rage!",
        "This is so unfair!",
        "I'm livid and seething!",
        "How dare they do this!",
        "I'm fed up with this!",
        "This is unacceptable!",
        "I'm enraged and hostile!",
        "So annoyed and aggravated!",
        "I'm losing my temper!",
        "This is provoking me!",
        "I'm bitter and resentful!",
        "What a nightmare!",
        "I'm ready to explode!",
        "This is disgusting!",
        "I'm offended and outraged!",
        "So irritating and vexing!",
        "I'm fuming mad!",
        "This is aggravating!",
        "I'm hostile and aggressive!",
        "What an insult!",
        "I'm worked up and angry!",
        "This is preposterous!"
    ],
    
    'sadness': [
        "I feel really sad and lonely",
        "This is so depressing",
        "I'm feeling down today",
        "Heartbroken and miserable",
        "So sad and disappointed",
        "Feeling blue and tearful",
        "Everything feels hopeless",
        "Crying and feeling low",
        "I'm grieving and sorrowful",
        "This is so heartbreaking",
        "Feeling empty and hollow",
        "I'm in despair",
        "So melancholy and gloomy",
        "I feel abandoned",
        "This is so painful",
        "I'm mourning and hurting",
        "Feeling dejected and defeated",
        "I'm crushed and devastated",
        "So lonely and isolated",
        "I feel worthless",
        "This brings me to tears",
        "I'm feeling heavy and burdened",
        "So pitiful and sorry",
        "I'm in anguish",
        "Feeling lost and alone",
        "This is so tragic",
        "I'm feeling vulnerable",
        "So discouraged and disheartened",
        "I feel like giving up",
        "This is so grim"
    ],
    
    'fear': [
        "I'm worried about the future",
        "This is scary and frightening",
        "I'm anxious and nervous",
        "Feeling terrified and panicked",
        "So afraid and worried",
        "This makes me nervous",
        "I'm scared of what might happen",
        "Feeling anxious and fearful",
        "I'm trembling with fear",
        "This is alarming!",
        "I'm apprehensive and uneasy",
        "Feeling threatened and endangered",
        "I'm petrified and horrified",
        "This is unsettling",
        "I'm feeling insecure",
        "So concerned and troubled",
        "I'm panicking and freaking out",
        "This is menacing",
        "I'm feeling vulnerable to danger",
        "What if something bad happens?",
        "I'm feeling unsafe",
        "This is ominous and foreboding",
        "I'm feeling pressured",
        "So startled and shocked",
        "I'm feeling trapped",
        "This is overwhelming",
        "I'm feeling exposed",
        "So doubtful and uncertain",
        "I'm feeling at risk",
        "This is intimidating"
    ],
    
    'neutral': [
        "The weather is okay",
        "Just another regular day",
        "Nothing special happening",
        "Feeling normal today",
        "It's an average day",
        "Everything is fine",
        "No strong feelings",
        "Just feeling normal",
        "I'm doing alright",
        "This is typical",
        "Feeling steady and stable",
        "Nothing out of the ordinary",
        "I'm calm and composed",
        "This is standard",
        "Feeling balanced",
        "I'm okay with this",
        "Just routine",
        "Feeling even-tempered",
        "This is ordinary",
        "I'm feeling平和",
        "Nothing to report",
        "Feeling content",
        "I'm relaxed",
        "This is expected",
        "Feeling at ease",
        "I'm comfortable",
        "Just passing time",
        "Feeling indifferent",
        "This is familiar",
        "I'm feeling baseline"
    ]
}


def train_and_save_model(model_path: str = None, n_components: int = 5, n_iterations: int = 100):
    """
    Train HMM classifier and save to file
    
    Args:
        model_path: Path to save the trained model
        n_components: Number of hidden states in HMM
        n_iterations: Number of EM iterations for training
    """
    if model_path is None:
        model_path = backend_dir / "nlp" / "models" / "hmm_emotion_model.pkl"
    
    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    print("=" * 60)
    print("HMM Emotion Classifier Training")
    print("=" * 60)
    
    print(f"\nTraining data statistics:")
    for emotion, texts in TRAINING_DATA.items():
        print(f"  {emotion}: {len(texts)} samples")
    
    print(f"\nModel configuration:")
    print(f"  Hidden states (n_components): {n_components}")
    print(f"  Feature dimensions: 30")
    print(f"  Training iterations: {n_iterations}")
    
    print("\n" + "-" * 60)
    print("Training started...")
    print("-" * 60)
    
    # Create and train classifier
    classifier = HMMEmotionClassifier(n_components=n_components, n_features=30)
    classifier.train(TRAINING_DATA, n_iterations=n_iterations)
    
    # Save the model
    classifier.save(model_path)
    
    # Test with sample data
    print("\n" + "-" * 60)
    print("Testing trained model...")
    print("-" * 60)
    
    test_texts = [
        ("I am so happy today!", "joy"),
        ("This makes me so angry!", "anger"),
        ("I feel really sad and lonely", "sadness"),
        ("I'm worried about the future", "fear"),
        ("The weather is okay", "neutral")
    ]
    
    correct = 0
    for text, expected in test_texts:
        result = classifier.detect(text)
        predicted = result['emotion']
        confidence = result['confidence']
        match = "✓" if predicted == expected else "✗"
        
        if predicted == expected:
            correct += 1
        
        print(f"\n{match} Text: {text}")
        print(f"  Expected: {expected}, Predicted: {predicted} ({confidence:.3f})")
    
    accuracy = correct / len(test_texts) * 100
    print(f"\n" + "=" * 60)
    print(f"Test Accuracy: {correct}/{len(test_texts)} ({accuracy:.1f}%)")
    print(f"Model saved to: {model_path}")
    print("=" * 60)
    
    return classifier


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train HMM Emotion Classifier")
    parser.add_argument("--n_components", type=int, default=3,
                        help="Number of hidden states in HMM")
    parser.add_argument("--n_iterations", type=int, default=100,
                        help="Number of EM iterations")
    parser.add_argument("--output", type=str, default=None,
                        help="Output path for trained model")

    args = parser.parse_args()

    train_and_save_model(
        model_path=args.output,
        n_components=args.n_components,
        n_iterations=args.n_iterations
    )
