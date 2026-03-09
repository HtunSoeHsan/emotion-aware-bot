"""
HMM-based Emotion Classifier
Uses Hidden Markov Models for sequence-based emotion detection from text
"""

import pickle
import os
import numpy as np
from typing import Dict, Tuple, List, Optional
from hmmlearn import hmm
from sklearn.preprocessing import StandardScaler


class HMMEmotionClassifier:
    """
    Emotion classifier using Hidden Markov Models
    
    Each emotion has its own HMM model trained on word sequences.
    Classification is done by computing log-likelihood of the sequence
    under each emotion's HMM and selecting the highest.
    """
    
    EMOTIONS = ['joy', 'anger', 'sadness', 'fear', 'neutral']
    
    # Emotion emojis for UI
    EMOTION_EMOJIS = {
        'joy': '😊',
        'anger': '😠',
        'sadness': '😢',
        'fear': '😨',
        'neutral': '😐'
    }
    
    # Color codes for UI (Tailwind CSS)
    EMOTION_COLORS = {
        'joy': 'green',
        'anger': 'red',
        'sadness': 'blue',
        'fear': 'purple',
        'neutral': 'gray'
    }
    
    def __init__(self, n_components: int = 3, n_features: int = 30):
        """
        Initialize HMM classifier
        
        Args:
            n_components: Number of hidden states in each HMM
            n_features: Dimensionality of word embeddings
        """
        self.n_components = n_components
        self.n_features = n_features
        self.models: Dict[str, hmm.GaussianHMM] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.word_to_idx: Dict[str, int] = {}
        self.idx_to_word: Dict[int, str] = {}
        self.is_trained = False
        
    def _text_to_sequence(self, text: str) -> np.ndarray:
        """
        Convert text to word index sequence
        
        Args:
            text: Input text
            
        Returns:
            Numpy array of word indices
        """
        import nltk
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        
        # Tokenize and remove stopwords
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words and t.isalpha()]
        
        # Convert to indices (use 0 for unknown words)
        sequence = [self.word_to_idx.get(token, 0) for token in tokens]
        
        if len(sequence) == 0:
            sequence = [0]  # Default to unknown word
            
        return np.array(sequence).reshape(-1, 1)
    
    def _text_to_features(self, text: str) -> np.ndarray:
        """
        Convert text to feature sequence using sentiment-based embeddings
        
        Args:
            text: Input text
            
        Returns:
            Numpy array of shape (seq_length, n_features)
        """
        import nltk
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        
        # Tokenize and remove stopwords
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words and t.isalpha()]
        
        if len(tokens) == 0:
            tokens = ['unknown']
        
        # Initialize VADER for sentiment features
        analyzer = SentimentIntensityAnalyzer()
        
        # Create sentiment-based feature vectors
        features = []
        for token in tokens:
            # Get sentiment scores for the word
            scores = analyzer.polarity_scores(token)
            
            # Feature vector: [neg, neu, pos, compound, word_length_norm, position_norm]
            feature_vec = np.zeros(self.n_features)
            feature_vec[0] = scores['neg']
            feature_vec[1] = scores['neu']
            feature_vec[2] = scores['pos']
            feature_vec[3] = scores['compound']
            feature_vec[4] = len(token) / 20.0  # Normalized word length
            
            # Add character-level features (first 10 chars)
            for i, char in enumerate(token[:10]):
                feature_vec[5 + i] = ord(char) / 256.0
            
            # First/last letter features
            if len(token) > 0:
                feature_vec[15] = ord(token[0]) / 256.0
                feature_vec[16] = ord(token[-1]) / 256.0
            
            # Vowel/consonant ratio
            vowels = sum(1 for c in token.lower() if c in 'aeiou')
            feature_vec[17] = vowels / max(len(token), 1)
            
            features.append(feature_vec)
        
        return np.array(features)
    
    def train(self, training_data: Dict[str, List[str]], n_iterations: int = 100):
        """
        Train HMM models for each emotion
        
        Args:
            training_data: Dictionary mapping emotion to list of training texts
            n_iterations: Number of EM iterations for training
        """
        # Build vocabulary from all training data
        all_words = set()
        for emotion, texts in training_data.items():
            for text in texts:
                import nltk
                from nltk.tokenize import word_tokenize
                tokens = word_tokenize(text.lower())
                all_words.update(tokens)
        
        # Create word index mapping
        self.word_to_idx = {word: idx + 1 for idx, word in enumerate(sorted(all_words))}
        self.word_to_idx['<UNK>'] = 0
        self.idx_to_word = {idx: word for word, idx in self.word_to_idx.items()}
        
        # Train one HMM per emotion
        for emotion in self.EMOTIONS:
            if emotion not in training_data:
                print(f"Warning: No training data for {emotion}")
                continue
                
            texts = training_data[emotion]
            
            # Prepare sequences
            sequences = [self._text_to_features(text) for text in texts]
            
            # Concatenate sequences with length tracking
            lengths = [len(seq) for seq in sequences]
            X = np.vstack(sequences)
            
            # Fit Gaussian HMM
            model = hmm.GaussianHMM(
                n_components=self.n_components,
                covariance_type='diag',
                n_iter=n_iterations,
                random_state=42,
                verbose=False
            )
            
            model.fit(X, lengths=lengths)
            self.models[emotion] = model
            
        self.is_trained = True
        print(f"Trained HMM models for {len(self.models)} emotions")
    
    def predict(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict emotion from text
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (predicted_emotion, confidence, all_scores)
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")
        
        # Convert text to feature sequence
        X = self._text_to_features(text)
        
        # Compute log-likelihood for each emotion's HMM
        scores = {}
        for emotion, model in self.models.items():
            try:
                log_likelihood = model.score(X)
                scores[emotion] = log_likelihood
            except Exception as e:
                scores[emotion] = float('-inf')
        
        # Convert log-likelihoods to probabilities using softmax
        log_probs = np.array(list(scores.values()))
        log_probs = log_probs - np.max(log_probs)  # Numerical stability
        probs = np.exp(log_probs) / np.sum(np.exp(log_probs))
        
        # Get prediction
        emotion_idx = np.argmax(probs)
        predicted_emotion = list(scores.keys())[emotion_idx]
        confidence = float(probs[emotion_idx])
        
        # Normalize scores to 0-1 range
        score_dict = {emotion: float(prob) for emotion, prob in zip(scores.keys(), probs)}
        
        return predicted_emotion, confidence, score_dict
    
    def save(self, filepath: str):
        """Save trained model to file"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'models': self.models,
                'word_to_idx': self.word_to_idx,
                'idx_to_word': self.idx_to_word,
                'n_components': self.n_components,
                'n_features': self.n_features,
                'is_trained': self.is_trained
            }, f)
        print(f"Model saved to {filepath}")
    
    def load(self, filepath: str):
        """Load trained model from file"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.models = data['models']
            self.word_to_idx = data['word_to_idx']
            self.idx_to_word = data['idx_to_word']
            self.n_components = data['n_components']
            self.n_features = data['n_features']
            self.is_trained = data['is_trained']
        print(f"Model loaded from {filepath}")
    
    def detect(self, text: str) -> Dict:
        """
        Detect emotion from text (compatible with VADER interface)
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with emotion, confidence, emoji, and color
        """
        emotion, confidence, scores = self.predict(text)
        
        return {
            'emotion': emotion,
            'confidence': round(confidence, 3),
            'emoji': self.EMOTION_EMOJIS[emotion],
            'color': self.EMOTION_COLORS[emotion],
            'scores': {k: round(v, 3) for k, v in scores.items()},
            'method': 'hmm'
        }


# Singleton instance
_classifier: Optional[HMMEmotionClassifier] = None
_model_path: str = None


def get_classifier(auto_load: bool = True) -> HMMEmotionClassifier:
    """Get or create HMM classifier singleton
    
    Args:
        auto_load: If True, automatically load trained model if it exists
    """
    global _classifier, _model_path
    
    if _classifier is None:
        _classifier = HMMEmotionClassifier()
        
        # Auto-load trained model if it exists
        if auto_load:
            import os
            from pathlib import Path
            
            # Try to find the model file
            possible_paths = [
                Path(__file__).parent / "models" / "hmm_emotion_model.pkl",
                Path("backend/nlp/models/hmm_emotion_model.pkl"),
                Path("nlp/models/hmm_emotion_model.pkl"),
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        _classifier.load(str(path))
                        _model_path = str(path)
                        print(f"Auto-loaded HMM model from {path}")
                        break
                    except Exception as e:
                        print(f"Failed to load HMM model from {path}: {e}")
    
    return _classifier


def train_hmm_classifier(training_data: Dict[str, List[str]], save_path: str = None):
    """
    Train and optionally save HMM classifier
    
    Args:
        training_data: Dictionary mapping emotion to list of training texts
        save_path: Optional path to save trained model
    """
    global _classifier
    _classifier = HMMEmotionClassifier()
    _classifier.train(training_data)
    
    if save_path:
        _classifier.save(save_path)
    
    return _classifier


def load_hmm_classifier(load_path: str) -> HMMEmotionClassifier:
    """Load HMM classifier from file"""
    global _classifier
    _classifier = HMMEmotionClassifier()
    _classifier.load(load_path)
    return _classifier


def detect_emotion_hmm(text: str) -> Dict:
    """
    Convenience function to detect emotion using HMM
    
    Args:
        text: Input text
        
    Returns:
        Emotion detection result dictionary
    """
    return get_classifier().detect(text)


if __name__ == "__main__":
    # Test the HMM classifier
    print("Testing HMM Emotion Classifier")
    print("=" * 50)
    
    # Sample training data (in practice, use much larger dataset)
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
    
    # Train the classifier
    classifier = HMMEmotionClassifier(n_components=3, n_features=50)
    classifier.train(training_data, n_iterations=50)
    
    # Test the classifier
    test_texts = [
        "I am so happy today!",
        "This makes me so angry!",
        "I feel really sad and lonely",
        "I'm worried about the future",
        "The weather is okay"
    ]
    
    print("\nTest Results:")
    print("-" * 50)
    for text in test_texts:
        result = classifier.detect(text)
        print(f"\nText: {text}")
        print(f"Emotion: {result['emoji']} {result['emotion']} ({result['confidence']:.3f})")
        print(f"Color: {result['color']}")
        print(f"Method: {result['method']}")
