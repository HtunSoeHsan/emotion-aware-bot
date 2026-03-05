# 🧠 Emotion-Aware AI Chatbot

An intelligent chatbot that detects emotions from text or speech and provides personalized recommendations using NLTK and AI agents.

**University NLP Project - Complete System**

## 🎯 Features

- **Emotion Detection**: Analyzes text/speech to detect emotions (Joy, Anger, Sadness, Fear, Neutral)
- **Dual Input**: Support for both text and voice (speech-to-text)
- **Smart Recommendations**: AI-powered suggestions using Ollama LLM + rule-based fallback
- **Modern UI**: Built with Next.js 14, Tailwind CSS, and shadcn/ui
- **Real-time Chat**: Interactive chatbot interface with emotion-colored responses
- **Privacy-First**: Can run 100% locally (no external APIs required)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (Next.js 14 + Tailwind + shadcn/ui)           │
│  - Chat UI with emotion colors                          │
│  - Text + Voice input (Web Speech API)                  │
└────────────────────┬────────────────────────────────────┘
                     │ REST API
┌────────────────────▼────────────────────────────────────┐
│  Backend (FastAPI + Python)                             │
│  ├─ NLTK VADER → Emotion Detection                      │
│  ├─ SpeechRecognition → Speech-to-Text                  │
│  └─ Ollama LLM + Rules → Recommendations                │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
emotion-aware-bot/
├── frontend/              # Next.js application
│   ├── app/
│   ├── components/
│   │   ├── chat/
│   │   └── ui/
│   └── lib/
├── backend/
│   ├── main.py            # FastAPI server
│   ├── nlp/               # NLTK emotion detection
│   ├── ai/                # Ollama AI + fallback rules
│   └── speech/            # Speech-to-text
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Groq API key (free at https://console.groq.com/keys)

### 1. Get Groq API Key (Free & Fast!)

```bash
# Get your free API key at:
https://console.groq.com/keys

# Then add it to backend/.env
GROQ_API_KEY=your_key_here
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:4001](http://localhost:4001)

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/detect/text` | POST | Detect emotion from text |
| `/api/detect/voice` | POST | Detect emotion from voice audio |
| `/health` | GET | Health check |

### Example Request (Text)

```bash
curl -X POST http://localhost:8000/api/detect/text \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy today!", "use_ai": true}'
```

### Example Response

```json
{
  "text": "I am so happy today!",
  "emotion": "joy",
  "confidence": 0.85,
  "recommendations": {
    "send_message": "Share this happiness with someone!",
    "action": "Write this moment in your journal"
  },
  "source": "ai"
}
```

## 🎨 Emotion Colors

| Emotion | Color | VADER Score |
|---------|-------|-------------|
| 😊 Joy | Green | compound ≥ 0.6 |
| 😠 Anger | Red | compound ≤ -0.6 |
| 😢 Sadness | Blue | -0.6 < compound < -0.3 |
| 😨 Fear | Purple | -0.3 < compound < 0 |
| 😐 Neutral | Gray | -0.3 < compound < 0.3 |

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Beautiful UI components
- **Lucide Icons** - Modern icon library

### Backend
- **FastAPI** - Modern Python web framework
- **NLTK** - Natural Language Toolkit (VADER sentiment)
- **SpeechRecognition** - Speech-to-text conversion
- **Ollama** - Local LLM for smart recommendations

## 🎓 University Project Notes

### NLP Techniques Used
1. **VADER Sentiment Analysis** - Rule-based sentiment scoring
2. **Tokenization** - Breaking text into words
3. **Stopword Removal** - Filtering common words
4. **Semantic Analysis** - WordNet-based similarity (optional)

### AI/ML Components
1. **Rule-based Classifier** - Emotion detection from sentiment scores
2. **LLM Integration** - Ollama/Llama2 for contextual recommendations
3. **Fallback System** - Rule-based backup when AI fails

### Demo Tips
- Show both text and voice input
- Toggle AI on/off to compare recommendations
- Explain the hybrid architecture (NLTK + LLM)

## 📝 License

MIT License - Educational Project

## 👨‍💻 Author

University NLP Project - Emotion-Aware AI System
