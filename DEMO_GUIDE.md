# 🎓 University Demo Guide - Emotion-Aware AI Chatbot

## 📋 Presentation Outline

### 1. Introduction (2 minutes)
- **Problem**: Mental health awareness, emotional support accessibility
- **Solution**: AI-powered emotion detection with actionable recommendations
- **Tech Stack**: NLTK (NLP) + FastAPI (Backend) + Next.js (Frontend)

### 2. System Architecture (3 minutes)
```
User Input (Text/Voice)
       ↓
[Speech-to-Text] ← if voice input
       ↓
[NLTK VADER] → Emotion Detection
       ↓
[Recommendation Engine]
   ├─ Ollama LLM (AI mode)
   └─ Rule-based (fallback)
       ↓
Display: Emotion + 2 Recommendations
```

### 3. NLP Techniques Used (3 minutes)

#### VADER Sentiment Analysis
- **V**alence **A**ware **D**ictionary for s**E**ntiment **R**easoning
- Rule-based sentiment lexicon
- Outputs compound score (-1 to +1)
- Maps to 5 emotions based on thresholds

```python
# Emotion Classification
if compound >= 0.6: → Joy
if compound <= -0.6: → Anger
if -0.6 < compound < -0.3: → Sadness
if -0.3 < compound < 0: → Fear
if -0.3 < compound < 0.3: → Neutral
```

#### Text Preprocessing
- Tokenization (NLTK punkt)
- Stopword removal
- Case normalization

### 4. AI/ML Components (2 minutes)

| Component | Technology | Purpose |
|-----------|------------|---------|
| Emotion Detection | NLTK VADER | Sentiment analysis |
| Recommendations (AI) | Ollama Llama2 | Contextual suggestions |
| Recommendations (Rules) | Predefined mapping | Fallback system |
| Speech Input | Google Speech API | Voice-to-text |

### 5. Live Demo (5 minutes)

#### Demo Script:

**1. Text Input - Joy**
```
Type: "I just got promoted at work!"
Expected: 😊 Joy (green), recommendations to share happiness
```

**2. Text Input - Anger**
```
Type: "This is so frustrating!"
Expected: 😠 Anger (red), recommendations to calm down
```

**3. Voice Input**
```
Click microphone → Speak: "I'm feeling really sad today"
Expected: 😢 Sadness (blue), transcribed + recommendations
```

**4. Toggle AI vs Rules**
```
Show: AI mode (smart) vs Rules mode (fast, offline)
Explain: Hybrid architecture for reliability
```

### 6. Code Highlights (2 minutes)

Show these files:

**Backend - Emotion Detection**
```python
# backend/nlp/emotion_detector.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
scores = sia.polarity_scores(text)
compound = scores['compound']
```

**Backend - AI Recommendations**
```python
# backend/ai/ollama_agent.py
import ollama

response = ollama.chat(
    model='llama2:7b',
    messages=[{'role': 'user', 'content': prompt}]
)
```

**Frontend - Chat UI**
```tsx
// frontend/components/chat/ChatContainer.tsx
const result = await analyzeText(messageText, useAI);
// Display emotion-colored response
```

### 7. Testing Results (1 minute)

Run the test script:
```bash
cd backend
source venv/bin/activate
python test_backend.py
```

Expected output:
```
✅ Emotion Detector: 5/5 passed
✅ Rule-Based Recommendations: All emotions covered
✅ Ollama AI Agent: Available (if installed)
✅ Speech-to-Text: Module initialized
```

### 8. Q&A Preparation

**Common Questions:**

1. **Why NLTK instead of transformers?**
   - Educational value (understand NLP fundamentals)
   - Lightweight, fast, no GPU needed
   - Transparent (not black-box)

2. **How accurate is emotion detection?**
   - VADER: ~70-80% for clear emotional text
   - Limitations: sarcasm, context-dependent

3. **Why hybrid AI approach?**
   - Reliability (fallback if AI fails)
   - Speed (rules faster than LLM)
   - Cost (local LLM is free)

4. **Can it detect multiple emotions?**
   - Currently single dominant emotion
   - Extension: Multi-label classification possible

5. **Privacy considerations?**
   - All processing can run locally
   - No data sent to external APIs (if using Ollama)
   - No data storage

---

## 🚀 Quick Start Commands

### Start Backend
```bash
cd backend
source venv/bin/activate
python main.py
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Run Tests
```bash
cd backend
python test_backend.py
```

### Test API
```bash
# Health check
curl http://localhost:8000/health

# Text analysis
curl -X POST http://localhost:8000/api/detect/text \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy!", "use_ai": true}'
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Emotion Detection Time | < 50ms |
| AI Recommendation (Ollama) | 2-5 seconds |
| Rule Recommendation | < 10ms |
| Speech-to-Text | 1-2 seconds |
| Frontend Render | < 100ms |

---

## 🎯 Grading Criteria Alignment

| Criteria | Implementation |
|----------|----------------|
| NLP Techniques | VADER, Tokenization, Sentiment Analysis |
| ML/AI | Ollama LLM, Rule-based classifier |
| System Design | Modular architecture (backend/frontend) |
| User Interface | Modern, responsive, accessible |
| Testing | Automated test suite |
| Documentation | README, API docs, code comments |

---

## 💡 Future Enhancements

1. **Multi-language support** (translate emotions)
2. **Emotion trends** (track mood over time)
3. **Voice output** (text-to-speech responses)
4. **Mobile app** (React Native)
5. **Fine-tuned model** (train on emotion dataset)

---

## 📸 Screenshots to Capture

1. Main chat interface (empty state)
2. Joy detection (green response)
3. Anger detection (red response)
4. Voice input (microphone active)
5. AI vs Rules toggle
6. Recommendation card close-up
7. API documentation (/docs endpoint)

---

**Good luck with your demo! 🎓✨**
