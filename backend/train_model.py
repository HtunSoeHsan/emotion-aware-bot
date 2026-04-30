import os
import sys
import json
from nlp.hmm_classifier import train_hmm_classifier

def main():
    print("🧠 Starting HMM Emotion Model Training (JSON Data)...")
    
    # Define paths
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "data", "emotion_data.json")
    model_dir = os.path.join(base_dir, "nlp", "models")
    save_path = os.path.join(model_dir, "hmm_emotion_model.pkl")
    
    # 1. Load JSON Data
    if not os.path.exists(json_path):
        print(f"❌ Error: {json_path} not found.")
        return
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
        print(f"✅ JSON data loaded (Total Emotions: {len(training_data)})")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return
    
    # 2. Create Model Directory
    os.makedirs(model_dir, exist_ok=True)
    
    # 3. Perform Training
    print("⏳ Training in progress... Please wait.")
    try:
        train_hmm_classifier(training_data, save_path=save_path)
        print(f"🎉 Training completed successfully!")
        print(f"📂 Model saved at: {save_path}")
        print("\n💡 Hint: Restart your Backend server to use the new model.")
    except Exception as e:
        print(f"❌ Training Error: {e}")

if __name__ == "__main__":
    main()
