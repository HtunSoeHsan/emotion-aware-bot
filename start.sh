#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       🧠 Emotion-Aware Bot - Quick Start                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Ollama is running
echo "🔍 Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  ✅ Ollama is running"
    echo "  📦 Available models:"
    ollama ls | grep -E "llama2|llama3|mistral" | while read line; do
        echo "     - $line"
    done
else
    echo "  ⚠️  Ollama is not running. Starting it..."
    ollama serve &
    sleep 2
fi

echo ""
echo "🔧 Starting Backend..."
cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "  Installing Python dependencies..."
    pip install -q -r requirements.txt
fi

# Download NLTK data if needed
python3 -c "import nltk; nltk.download('vader_lexicon', quiet=True); nltk.download('punkt', quiet=True)" 2>/dev/null

echo "  ✅ Backend ready"
echo ""
echo "🚀 Starting FastAPI server..."
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Backend running at: http://localhost:8000               ║"
echo "║  API Docs: http://localhost:8000/docs                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "💡 In a NEW terminal, run:"
echo "   cd frontend && npm run dev"
echo ""
echo "Press Ctrl+C to stop the backend"
echo ""

# Start the server
python main.py
