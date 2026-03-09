# 🌏 Myanmar-Specific External Resource Integration

**Real-time recommendations from YouTube, Myanmar music, news, and local content sources**

---

## 🔄 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  User Input (Myanmar): "ကျွန်တော် စိတ်ညစ်နေတယ်" (I'm stressed)  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. Emotion Detection                                           │
│     - HMM/VADER analyzes text                                   │
│     - Result: sadness/fear (confidence: 0.85)                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Query Builder (Multi-language)                              │
│     - Emotion: fear/sadness                                     │
│     - Context keywords: stress, worry                           │
│     - Myanmar queries: "စိတ်ငြိမ်", "တရားတော်"                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. External API Calls (Parallel - No API Key Required)         │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐      │
│  │   YouTube      │ │  YouTube Music │ │   Myanmar      │      │
│  │   Videos       │ │  (Myanmar)     │ │   News Sites   │      │
│  │   - Meditation │ │  - သီချင်းများ    │ │   - Eleven     │      │
│  │   - Dhamma     │ │  - တရားတော်များ   │ │   - Mizzima    │      │
│  │   - Calming    │ │  - Acoustic    │ │   - Irrawaddy  │      │
│  └────────────────┘ └────────────────┘ └────────────────┘      │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐      │
│  │   Spotify      │ │   Podcasts     │ │   TED Talks    │      │
│  │   (Global)     │ │   (iTunes)     │ │   (Curated)    │      │
│  │   - Playlists  │ │  - Episodes    │ │   - Talks      │      │
│  └────────────────┘ └────────────────┘ └────────────────┘      │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Response Processing                                         │
│     - Mix Myanmar + International content                       │
│     - Add direct URLs (no authentication needed)                │
│     - Cache for 6 hours (reduce API calls)                      │
│     - Fallback to curated list if API fails                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. Rich Recommendations with Live Links                        │
│  {                                                              │
│    "youtube": [                                                 │
│      {"title": "5-Min Breathing", "url": "youtube.com/..."},   │
│      {"title": "မြန်မာတရားတော်", "url": "youtube.com/..."}       │
│    ],                                                           │
│    "youtube_music": [                                           │
│      {"title": "Myanmar Calming Songs",                         │
│       "url": "youtube.com/results?search_query=...",            │
│       "description": "စိတ်ငြိမ်အေးစေသောသီချင်းများ"}            │
│    ],                                                           │
│    "news": [                                                    │
│      {"title": "Mental Health Awareness",                       │
│       "url": "myanmarmentalhealth.org",                         │
│       "source": "MM Mental Health"}                             │
│    ]                                                            │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Myanmar-Specific Sources

### 1. 🎵 Myanmar Music (YouTube Music)

**No API key required** - Uses YouTube search URLs

| Emotion | Myanmar Search Query | Description |
|---------|---------------------|-------------|
| Joy | `myanmar happy songs` | မြန်မာသီချင်းပျော်ရွှင်စရာများ |
| Joy | `myanmar pop songs 2024` | နောက်ဆုံးထွက်မြန်မာပေါ့ပ်သီချင်းများ |
| Anger | `myanmar calming music` | စိတ်ငြိမ်အေးစေသောသီချင်းများ |
| Anger | `myanmar buddha chanting` | တရားတော်နှင့်သီချင်းများ |
| Sadness | `myanmar sad songs` | မြန်မာသီချင်းစိတ်ဓာတ်ကျစရာများ |
| Sadness | `myanmar love ballads` | အချစ်သီချင်းများ |
| Fear | `myanmar meditation music` | တရားထိုင်ဂီတ |
| Fear | `myanmar dhamma talks` | တရားတော်များ |
| Neutral | `myanmar lofi music` | မြန်မာလိုဖိုင်းဂီတ |
| Neutral | `myanmar study music` | စာကျက်ဂီတ |

**Example URLs:**
```
https://www.youtube.com/results?search_query=myanmar+calming+music
https://www.youtube.com/results?search_query=myanmar+meditation+music
```

---

### 2. 📰 Myanmar News Sources

**Curated links** - No API required

| Emotion | Source | URL | Description |
|---------|--------|-----|-------------|
| Joy | Myanmar Times | `mmtimes.com` | Success stories |
| Joy | GoMyanmar | `gomymyanmar.com` | Culture & arts |
| Anger | The Irrawaddy | `irrawaddy.com` | Peace building |
| Anger | Mizzima | `mizzima.com` | Conflict resolution |
| Sadness | Myanmar Mental Health | `myanmarmentalhealth.org` | Mental health support |
| Sadness | DVB | `dvb.no` | Hope stories |
| Fear | Ministry of Health | `health.gov.mm` | Health advisories |
| Fear | Myanmar Health | `myanmarhealth.org` | Stress management |
| Neutral | Eleven Media | `elevenmyanmar.com` | Current affairs |
| Neutral | Myanmar IT | `myanmarit.com` | Technology news |

---

### 3. 📺 YouTube Videos (with API or Fallback)

**With YouTube API Key:**
- Real-time video search
- Thumbnail images
- Channel information
- Video descriptions

**Without API Key (Fallback):**
- Curated video list
- Direct YouTube URLs
- Always available

**Example Myanmar Content:**
```python
'fear': [
    {'title': '5-4-3-2-1 Grounding Technique', 
     'url': 'https://www.youtube.com/watch?v=Q1HH1qZzCqM'},
    {'title': 'Myanmar Meditation Guide',
     'url': 'https://www.youtube.com/results?search_query=myanmar+meditation'}
]
```

---

### 4. 🎧 Podcasts (iTunes API)

**Free iTunes API** - No authentication required

```python
# Search for podcasts
https://itunes.apple.com/search?term=meditation&media=podcast&limit=5
```

**Myanmar-relevant searches:**
- `meditation`
- `mindfulness`
- `dhamma`
- `mental health`
- `self improvement`

---

## 🔧 Implementation

### File Structure
```
backend/ai/
├── external_resource_recommender.py    # Main external API integration
├── multi_source_recommender.py         # Static recommendations
└── fallback_rules.py                   # Rule-based fallback
```

### Key Functions

```python
# Get all external recommendations
recs = get_external_recommendations(
    emotion='fear',
    context='I'm worried about my exam',
    sources=['youtube', 'spotify', 'podcast', 'news', 'ted']
)

# Returns:
{
    'emotion': 'fear',
    'sources': {
        'youtube': [...],      # Video links
        'spotify': [...],      # Spotify + Myanmar music
        'podcast': [...],      # Podcast episodes
        'news': [...],         # Myanmar + International news
        'ted': [...]           # TED talks
    },
    'quick_picks': {           # First item from each source
        'youtube': {...},
        'spotify': {...},
        ...
    }
}
```

---

## 🚀 API Usage

### Endpoint
```
POST /api/detect/text
```

### Request
```json
{
  "text": "ကျွန်တော် စိတ်ဖိစီးနေတယ်",
  "method": "hmm"
}
```

### Response (with External Resources)
```json
{
  "emotion": "fear",
  "confidence": 0.85,
  "external_resources": {
    "emotion": "fear",
    "sources": {
      "youtube": [
        {
          "title": "5-Minute Anxiety Relief",
          "url": "https://www.youtube.com/watch?v=...",
          "thumbnail": "https://img.youtube.com/vi/.../mqdefault.jpg",
          "source": "youtube"
        },
        {
          "title": "Myanmar Meditation Music",
          "url": "https://www.youtube.com/results?search_query=myanmar+meditation",
          "description": "တရားထိုင်ဂီတ",
          "source": "youtube_music"
        }
      ],
      "spotify": [
        {
          "title": "Anxiety Relief",
          "url": "https://open.spotify.com/playlist/...",
          "source": "spotify"
        },
        {
          "title": "Myanmar Calming Songs",
          "url": "https://www.youtube.com/results?search_query=myanmar+calming+music",
          "description": "စိတ်ငြိမ်အေးစေသောသီချင်းများ",
          "source": "youtube_music"
        }
      ],
      "news": [
        {
          "title": "Mental Health Awareness Myanmar",
          "url": "https://www.myanmarmentalhealth.org/",
          "source": "MM Mental Health",
          "description": "Mental health resources"
        }
      ]
    },
    "quick_picks": {
      "youtube": {...},
      "spotify": {...},
      "news": {...}
    }
  }
}
```

---

## 📦 Setup

### 1. Install Dependencies
```bash
cd backend
pip install requests
```

### 2. Environment Variables (Optional)
```bash
# backend/.env

# YouTube API (optional - has fallback without it)
YOUTUBE_API_KEY=your_key_here

# Spotify (not needed - uses direct links)
# Spotify (not needed - uses iTunes API)
# News API (not needed - uses curated Myanmar sources)
```

### 3. Test
```bash
python ai/external_resource_recommender.py
```

---

## ✅ Advantages of This Approach

### No API Keys Required (Mostly)
- ✅ YouTube: Works with fallback URLs
- ✅ Myanmar Music: YouTube search links
- ✅ Myanmar News: Curated direct links
- ✅ Podcasts: Free iTunes API
- ✅ TED: Curated list

### Myanmar-Friendly
- ✅ Myanmar language search queries
- ✅ Local news sources
- ✅ Buddhist dhamma content
- ✅ Cultural relevance

### Caching
- ✅ 6-hour cache reduces API calls
- ✅ Faster response times
- ✅ Works offline (cached data)

### Fallback System
- ✅ API fails → Use curated list
- ✅ Always returns something
- ✅ Graceful degradation

---

## 🎯 Example Use Cases

### Case 1: User Feeling Anxious (Myanmar)
```
Input: "ကျွန်တော် စိတ်ပူနေတယ်" (I'm worried)

Recommendations:
- YouTube: Myanmar meditation music
- Music: Buddha chanting, acoustic songs
- News: Mental health awareness Myanmar
- Podcast: Dhamma talks
- Activity: 5-4-3-2-1 grounding technique
```

### Case 2: User Feeling Sad
```
Input: "ဝမ်းနည်းနေတယ်" (I'm sad)

Recommendations:
- YouTube: Comforting Myanmar songs
- Music: Myanmar ballads
- News: Community support stories
- Podcast: Healing episodes
- Activity: Call a loved one
```

### Case 3: User Feeling Stressed
```
Input: "စိတ်ဖိစီးနေတယ်" (I'm stressed)

Recommendations:
- YouTube: Breathing exercises
- Music: Calming Myanmar instrumental
- News: Stress management guides
- Podcast: Mindfulness episodes
- Activity: Progressive muscle relaxation
```

---

## 📈 Future Enhancements

### Planned Features
1. **Facebook Integration** - Myanmar popular platform
2. **TikTok Videos** - Short-form calming content
3. **Viber Stickers** - Emotional support stickers
4. **Myanmar Astrology** - Horoscope-based recommendations
5. **Local Events** - Meditation centers, temples
6. **Weather Integration** - Suggest indoor/outdoor activities

### Content Expansion
- More Myanmar artists
- Regional news sources
- Local mental health hotlines
- Burmese language podcasts
- Traditional healing practices

---

**Last Updated:** March 2026  
**Version:** 3.0.0 (Myanmar Integration)
