# Emotion-Aware Bot - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Option 1: Automated Setup

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"

# Start backend
python main.py
```

Backend runs on: http://localhost:8000

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend runs on: http://localhost:3000

---

## 🎯 Optional: Enable AI Recommendations

For smarter recommendations using local LLM:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download Llama2 model (4GB)
ollama pull llama2:7b

# Ollama runs automatically on http://localhost:11434
```

---

## 📡 API Endpoints

### Test with curl:

```bash
# Text analysis
curl -X POST http://localhost:8000/api/detect/text \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy today!", "use_ai": true}'

# Health check
curl http://localhost:8000/health
```

---

## 🎮 Usage

1. **Open** http://localhost:3000
2. **Type** a message or **click microphone** to speak
3. **View** detected emotion and color-coded response
4. **Get** 2 personalized recommendations:
   - Message to send to someone
   - Self-care action to take

---

## 🧪 Test Examples

Try these inputs:

| Emotion | Example Text |
|---------|-------------|
| 😊 Joy | "I just got promoted at work!" |
| 😠 Anger | "This is so frustrating!" |
| 😢 Sadness | "I feel really lonely today" |
| 😨 Fear | "I'm worried about my presentation" |
| 😐 Neutral | "Having a regular day" |

---

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check Python version (need 3.9+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Check Node version (need 18+)
node --version

# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

### Microphone not working
- Allow microphone permission in browser
- Check browser settings
- Try Chrome/Edge (best Web Speech API support)

### Ollama not available
- The system falls back to rule-based recommendations automatically
- No error, just less personalized suggestions

---

## 📚 Project Structure

```
emotion-aware-bot/
├── backend/              # FastAPI + NLTK + Ollama
│   ├── main.py          # API server
│   ├── nlp/             # Emotion detection
│   ├── ai/              # AI recommendations
│   └── speech/          # Speech-to-text
├── frontend/            # Next.js + Tailwind
│   ├── app/             # Pages
│   ├── components/      # UI components
│   └── lib/             # API client
└── README.md
```

---

## 🎓 For University Demo

**Key Points to Highlight:**

1. **NLTK VADER** - Traditional NLP sentiment analysis
2. **Hybrid AI** - Ollama LLM + rule-based fallback
3. **Speech Input** - Web Speech API integration
4. **Real-time UI** - Emotion-colored responses
5. **Privacy-First** - All processing can run locally

**Architecture Explanation:**
```
Input → Speech-to-Text (if voice) → NLTK Emotion Detection 
      → AI/Rules Recommendation → Colored UI Response
```

---

## 📄 License

MIT License - Educational Project
