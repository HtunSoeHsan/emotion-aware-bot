#!/bin/bash

# 🧠 Emotion-Aware Bot - Universal Installation Script

echo "============================================================"
echo "       🧠 Emotion-Aware Bot Installation                    "
echo "============================================================"

# 1. Setup Backend
echo "📦 Setting up Backend..."
cd backend || { echo "❌ Error: backend directory not found."; exit 1; }

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating Virtual Environment..."
    python3 -m venv venv
fi

# Activate and Install
echo "🔌 Activating environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cd ..

# 2. Setup Frontend
echo "🎨 Setting up Frontend..."
cd frontend || { echo "❌ Error: frontend directory not found."; exit 1; }

if [ -f "yarn.lock" ]; then
    echo "🧶 Installing with Yarn..."
    yarn install
else
    echo "📦 Installing with NPM..."
    npm install
fi

cd ..

echo "------------------------------------------------------------"
echo "✅ Installation Completed Successfully!"
echo "🚀 To start the app, run: ./start.sh"
echo "------------------------------------------------------------"
