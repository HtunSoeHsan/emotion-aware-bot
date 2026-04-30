#!/bin/bash

# 🧠 Emotion-Aware Bot - HMM Training Script

echo "============================================================"
echo "       🧠 HMM Emotion Model Training                        "
echo "============================================================"

# 1. Navigate to backend
cd backend || { echo "❌ Error: backend directory not found."; exit 1; }

# 2. Check Virtual Environment
if [ -d "venv" ]; then
    echo "🔧 Using Virtual Environment..."
    source venv/bin/activate
else
    echo "⚠️  Warning: venv not found. Using global python."
fi

# 3. Run Training Script
python train_model.py

# 4. Finish
echo "------------------------------------------------------------"
echo "✅ Training Completed Successfully!"
echo "💡 Please Restart the Backend to apply changes."
echo "------------------------------------------------------------"
