# 🎁 Multi-Source Recommendation System

**Comprehensive emotion-based recommendations across 8 different source types**

---

## 📋 Overview

The Emotion-Aware Bot now provides **multi-source recommendations** tailored to your emotional state. Instead of just one suggestion, you get personalized recommendations across:

- 🎵 **Music** - Songs and playlists
- 🎧 **Podcasts** - Relevant episodes
- 📺 **Videos** - TED talks, YouTube content
- ✨ **Activities** - Actionable exercises
- 📚 **Books** - Reading recommendations
- 📱 **Apps** - Helpful mobile applications
- 👥 **Social** - Connection suggestions
- 💆 **Self-Care** - Wellness activities

---

## 🚀 API Response Example

### Request
```bash
curl -X POST http://localhost:8000/api/detect/text \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling sad today", "method": "hmm"}'
```

### Response Structure
```json
{
  "text": "I am feeling sad today",
  "emotion": "sadness",
  "confidence": 0.999,
  "emoji": "😢",
  "color": "blue",
  "recommendations": {
    "send_message": "Hey, I'm not feeling great today...",
    "action": "Take a 10-minute walk outside..."
  },
  "source": "ai",
  "scores": {...},
  "method": "hmm",
  "multi_source": {
    "emotion": "sadness",
    "sources": {
      "music": [
        {
          "title": "Fix You - Coldplay",
          "type": "song",
          "description": "Emotional healing"
        }
      ],
      "podcast": [
        {
          "title": "The Sad, Sad Podcast",
          "episode": "Processing Grief",
          "description": "Mental health discussions"
        }
      ],
      "video": [
        {
          "title": "The Power of Vulnerability",
          "platform": "TED Talk",
          "duration": "20 min",
          "description": "Brené Brown's classic"
        }
      ],
      "activity": [
        {
          "title": "Cozy Blanket Time",
          "description": "Wrap up and rest without guilt",
          "duration": "30-60 min",
          "effort": "low"
        }
      ],
      "self_care": [
        "Practice gentle self-compassion meditation",
        "Allow yourself to cry if needed",
        "Take a warm bath with Epsom salts"
      ]
    },
    "quick_action": {
      "title": "Warm Beverage Ritual",
      "description": "Make tea or hot chocolate mindfully",
      "duration": "10-15 min",
      "effort": "low"
    },
    "send_message": "Let someone know you need a check-in call"
  }
}
```

---

## 📊 Source Types Breakdown

### 1. 🎵 Music
**Purpose:** Mood regulation through music therapy

**Examples by Emotion:**

| Emotion | Song | Artist | Description |
|---------|------|--------|-------------|
| Joy | "Happy" | Pharrell Williams | Upbeat pop anthem |
| Anger | "Weightless" | Marconi Union | Scientifically calming |
| Sadness | "Fix You" | Coldplay | Emotional healing |
| Fear | "Brave" | Sara Bareilles | Empowering anthem |
| Neutral | "Lo-Fi Beats" | Playlist | Chill background |

---

### 2. 🎧 Podcasts
**Purpose:** Educational and supportive audio content

**Examples by Emotion:**

| Emotion | Podcast | Episode | Description |
|---------|---------|---------|-------------|
| Joy | The Happiness Lab | Finding Joy | Science of happiness |
| Anger | Ten Percent Happier | Working with Anger | Buddhist perspective |
| Sadness | Terrible, Thanks for Asking | It's Okay to Not Be Okay | Honest conversations |
| Fear | The Anxiety Coaches | Calming Panic | Expert advice |
| Neutral | Stuff You Should Know | Random Topics | Educational fun |

---

### 3. 📺 Videos
**Purpose:** Visual learning and inspiration

**Examples by Emotion:**

| Emotion | Title | Platform | Duration |
|---------|-------|----------|----------|
| Joy | The Science of Happiness | TED Talk | 12 min |
| Anger | 5-Minute Anger Management | YouTube | 5 min |
| Sadness | The Power of Vulnerability | TED Talk | 20 min |
| Fear | 5-4-3-2-1 Grounding Technique | YouTube | 5 min |
| Neutral | How to Build Better Habits | TED Talk | 15 min |

---

### 4. ✨ Activities
**Purpose:** Actionable exercises with time/effort estimates

**Structure:**
```json
{
  "title": "Box Breathing",
  "description": "Inhale 4s, hold 4s, exhale 4s, hold 4s",
  "duration": "3-5 min",
  "effort": "low"
}
```

**Examples by Emotion:**

| Emotion | Activity | Duration | Effort |
|---------|----------|----------|--------|
| Joy | Dance Party | 10-15 min | Low |
| Anger | Write & Release | 10 min | Low |
| Sadness | Call a Loved One | 15-30 min | Medium |
| Fear | 5-4-3-2-1 Grounding | 3-5 min | Low |
| Neutral | Learn Something New | 20-30 min | Medium |

---

### 5. 📚 Books
**Purpose:** Deep reading for understanding and growth

**Examples by Emotion:**

| Emotion | Title | Author | Description |
|---------|-------|--------|-------------|
| Joy | The Happiness Project | Gretchen Rubin | Year-long journey |
| Anger | Anger: Wisdom for Cooling the Flames | Thich Nhat Hanh | Buddhist approach |
| Sadness | Reasons to Stay Alive | Matt Haig | Memoir of survival |
| Fear | Feel the Fear and Do It Anyway | Susan Jeffers | Classic self-help |
| Neutral | Atomic Habits | James Clear | Building habits |

---

### 6. 📱 Apps
**Purpose:** Digital tools for ongoing support

**Examples by Emotion:**

| Emotion | App | Category | Description |
|---------|-----|----------|-------------|
| Joy | Daylio | Journal | Mood tracking |
| Anger | Calm | Meditation | Anger management |
| Sadness | Woebot | Mental Health | AI therapy chatbot |
| Fear | Dare | Mental Health | Anxiety relief |
| Neutral | Duolingo | Education | Learn languages |

---

### 7. 👥 Social
**Purpose:** Connection and communication suggestions

**Examples by Emotion:**

| Emotion | Suggestion |
|---------|------------|
| Joy | "Share your happiness on social media to inspire others" |
| Anger | "Tell someone you need space right now" |
| Sadness | "Text a friend: 'Having a tough day, could use support'" |
| Fear | "Tell someone: 'I'm feeling anxious, can you help me talk through it?'" |
| Neutral | "Send a 'thinking of you' message to a friend" |

---

### 8. 💆 Self-Care
**Purpose:** Personal wellness and comfort activities

**Examples by Emotion:**

| Emotion | Activity |
|---------|----------|
| Joy | "Take a celebratory bubble bath" |
| Anger | "Take a cool shower to reset" |
| Sadness | "Take a warm bath with Epsom salts" |
| Fear | "Use calming essential oils (lavender, bergamot)" |
| Neutral | "Drink a full glass of water" |

---

## 🔧 Implementation Details

### File Structure
```
backend/ai/
├── multi_source_recommender.py    # Main recommendation engine
├── fallback_rules.py               # Updated to use multi-source
├── groq_agent.py                   # AI recommendations
└── ollama_agent.py                 # Local LLM recommendations
```

### Key Classes

#### MultiSourceRecommender
```python
class MultiSourceRecommender:
    RECOMMENDATIONS = {
        'joy': {
            'music': [...],
            'podcast': [...],
            'video': [...],
            'activity': [...],
            'book': [...],
            'app': [...],
            'social': [...],
            'self_care': [...]
        },
        # ... other emotions
    }
    
    def get_recommendations(emotion, context, source_types, count):
        # Returns multi-source recommendations
```

### Usage

```python
from ai.multi_source_recommender import get_recommendations

# Get all sources
recs = get_recommendations(
    emotion='sadness',
    context='I miss my family',
    source_types=['music', 'video', 'activity'],
    count=3
)

# Get quick recommendation
quick = get_quick_recommendation(emotion='anger')
```

---

## 📈 Statistics

### Content per Emotion

| Source Type | Items per Emotion | Total (5 emotions) |
|-------------|-------------------|-------------------|
| Music | 5 songs | 25 songs |
| Podcast | 3 episodes | 15 episodes |
| Video | 3 videos | 15 videos |
| Activity | 6 exercises | 30 activities |
| Book | 3 recommendations | 15 books |
| App | 3 suggestions | 15 apps |
| Social | 4 suggestions | 20 suggestions |
| Self-Care | 4 activities | 20 activities |

**Total:** 155+ curated recommendations!

---

## 🎯 Features

### ✅ What's Included

1. **Emotion-Specific Content** - Different recommendations for each emotion
2. **Multi-Source Variety** - 8 different types of recommendations
3. **Quick Actions** - Single immediate activity suggestion
4. **Social Suggestions** - Ways to connect with others
5. **Time Estimates** - Duration for each activity
6. **Effort Levels** - Low/medium effort indicators
7. **Descriptions** - Clear explanation of each recommendation
8. **Randomization** - Varied suggestions on each request

### 🔄 Customization Options

```python
# Select specific source types
recs = get_recommendations(
    emotion='joy',
    source_types=['music', 'activity']  # Only these sources
)

# Adjust count per source
recs = get_recommendations(
    emotion='anger',
    count=5  # 5 items per source
)

# Get all available sources
sources = get_all_sources()
# Returns: ['music', 'podcast', 'video', 'activity', 'book', 'app', 'social', 'self_care']
```

---

## 🚀 Testing

### Test the Recommender
```bash
cd backend
source venv/bin/activate
python ai/multi_source_recommender.py
```

### Test via API
```bash
# Test with HMM
curl -X POST http://localhost:8000/api/detect/text \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy!", "method": "hmm"}' | python3 -m json.tool

# Test with VADER
curl -X POST http://localhost:8000/api/detect/text \
  -H "Content-Type: application/json" \
  -d '{"text": "I am angry!", "method": "vader"}' | python3 -m json.tool

# Test Hybrid
curl -X POST http://localhost:8000/api/detect/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Feeling neutral", "method": "hybrid"}' | python3 -m json.tool
```

---

## 🎓 Future Enhancements

### Planned Features
1. **Context-Aware Recommendations** - Use NLP to match specific situations
2. **User Feedback Loop** - Learn which recommendations work best
3. **Spotify/YouTube Integration** - Direct links to play content
4. **Personalization** - Remember user preferences
5. **Time-of-Day Awareness** - Suggest appropriate activities for time
6. **Location-Based** - Consider user's location for activities
7. **Weather Integration** - Indoor/outdoor activity suggestions

### Content Expansion
- Add more music genres per emotion
- Include guided meditations
- Add breathing exercise videos
- Include art therapy activities
- Add journaling prompts
- Include nutrition suggestions

---

## 📖 References

### Music Therapy Research
- Thaut, M. H. (2005). *Rhythm, Music and the Brain*
- Koelsch, S. (2014). "Brain correlates of music-evoked emotions"

### Activity-Based Interventions
- Behavioral Activation Therapy (Martell et al., 2001)
- Positive Psychology Interventions (Seligman, 2011)

### Digital Mental Health
- Torous, J. et al. (2021). "The growing world of mental health apps"

---

**Last Updated:** March 2026  
**Version:** 2.0.0 (Multi-Source Integration)
