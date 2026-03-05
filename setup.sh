#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       🧠 Emotion-Aware Bot - Setup Script                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "📦 Checking Python version..."
python3 --version

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"

cd ..

# Setup Frontend
echo ""
echo "🎨 Setting up Frontend..."
cd frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "Node.js version: $(node --version)"

# Install npm dependencies
echo "Installing npm dependencies..."
npm install

cd ..

# Create .env file for frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  ✅ Setup Complete!                      ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Next Steps:                                             ║"
echo "║                                                          ║"
echo "║  1. Install Ollama (optional for AI recommendations):    ║"
echo "║     curl -fsSL https://ollama.com/install.sh | sh        ║"
echo "║     ollama pull llama2:7b                                ║"
echo "║                                                          ║"
echo "║  2. Start Backend:                                       ║"
echo "║     cd backend && source venv/bin/activate               ║"
echo "║     python main.py                                       ║"
echo "║                                                          ║"
echo "║  3. Start Frontend (new terminal):                       ║"
echo "║     cd frontend && npm run dev                           ║"
echo "║                                                          ║"
echo "║  4. Open: http://localhost:3000                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
