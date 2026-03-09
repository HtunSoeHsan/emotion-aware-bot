"""
External Resource Recommendation Engine
Fetches real-time recommendations from YouTube, Spotify, News APIs, and more
"""

import requests
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import hashlib
from dotenv import load_dotenv

load_dotenv()


class ExternalResourceRecommender:
    """Fetch recommendations from external APIs"""

    # API Configuration
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    ITUNES_API_URL = "https://itunes.apple.com/search"

    # Cache for API responses (in-memory)
    _cache: Dict[str, Dict] = {}
    _cache_duration = timedelta(hours=6)  # Cache for 6 hours

    # Emotion-based search queries
    EMOTION_QUERIES = {
        'joy': {
            'youtube': ['uplifting music', 'happy songs', 'positive vibes playlist', 'feel good music'],
            'spotify': ['happy hits', 'feel good playlist', 'uplifting songs', 'good mood music'],
            'podcast': ['happiness', 'positive psychology', 'gratitude', 'joy'],
            'news': ['positive news', 'good news', 'uplifting stories'],
            'ted': ['happiness', 'positive psychology', 'joy', 'wellbeing']
        },
        'anger': {
            'youtube': ['anger management', 'calming music', 'stress relief', 'deep breathing'],
            'spotify': ['calming music', 'peaceful piano', 'stress relief', 'meditation music'],
            'podcast': ['anger management', 'emotional regulation', 'calm', 'patience'],
            'news': ['conflict resolution', 'peace building', 'mindfulness'],
            'ted': ['anger management', 'emotional intelligence', 'self-control']
        },
        'sadness': {
            'youtube': ['comforting music', 'healing songs', 'sadness support', 'emotional healing'],
            'spotify': ['comfort songs', 'healing music', 'sad songs', 'emotional support'],
            'podcast': ['depression support', 'mental health', 'grief', 'healing'],
            'news': ['mental health awareness', 'depression support', 'hope stories'],
            'ted': ['depression', 'mental health', 'resilience', 'hope']
        },
        'fear': {
            'youtube': ['anxiety relief', 'calming techniques', 'grounding exercises', 'panic attack help'],
            'spotify': ['anxiety relief', 'calming sounds', 'peaceful music', 'meditation'],
            'podcast': ['anxiety help', 'fear management', 'panic support', 'calm'],
            'news': ['anxiety tips', 'mental wellness', 'stress management'],
            'ted': ['anxiety', 'fear', 'courage', 'resilience']
        },
        'neutral': {
            'youtube': ['lofi beats', 'study music', 'relaxing sounds', 'peaceful music'],
            'spotify': ['lofi playlist', 'chill vibes', 'relaxing music', 'peaceful piano'],
            'podcast': ['educational', 'self improvement', 'learning', 'curiosity'],
            'news': ['science news', 'technology', 'education', 'culture'],
            'ted': ['learning', 'creativity', 'innovation', 'self improvement']
        }
    }

    def __init__(self):
        """Initialize external resource recommender"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EmotionAwareBot/1.0'
        })

    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """Get cached response if available and not expired"""
        if key in self._cache:
            cached = self._cache[key]
            if datetime.now() - cached['timestamp'] < self._cache_duration:
                return cached['data']
            else:
                del self._cache[key]
        return None

    def _save_to_cache(self, key: str, data: Dict):
        """Save response to cache"""
        self._cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }

    def _generate_cache_key(self, *args) -> str:
        """Generate unique cache key from arguments"""
        key_string = '|'.join(str(arg) for arg in args)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get_youtube_videos(self, emotion: str, context: str = "", limit: int = 5) -> List[Dict]:
        """
        Fetch relevant YouTube videos

        Args:
            emotion: Detected emotion
            context: Additional context for search
            limit: Number of videos to return

        Returns:
            List of video recommendations with titles, URLs, thumbnails
        """
        if not self.YOUTUBE_API_KEY:
            return self._get_fallback_youtube(emotion)

        cache_key = self._generate_cache_key('youtube', emotion, context, limit)
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        # Build search query
        queries = self.EMOTION_QUERIES.get(emotion, {}).get('youtube', ['calming music'])
        if context:
            queries.append(context)

        search_query = ' '.join(queries[:2])  # Use top 2 queries

        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': search_query,
                'type': 'video',
                'maxResults': limit,
                'key': self.YOUTUBE_API_KEY,
                'videoDuration': 'short',  # Prefer shorter videos (< 4 min)
                'relevanceLanguage': 'en'
            }

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            videos = []
            for item in data.get('items', []):
                snippet = item['snippet']
                video_id = item['id']['videoId']

                videos.append({
                    'title': snippet['title'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': snippet['thumbnails']['medium']['url'],
                    'channel': snippet['channelTitle'],
                    'description': snippet['description'][:200] + '...',
                    'source': 'youtube',
                    'emotion': emotion
                })

            self._save_to_cache(cache_key, videos)
            return videos

        except Exception as e:
            print(f"YouTube API error: {e}")
            return self._get_fallback_youtube(emotion)

    def _get_fallback_youtube(self, emotion: str) -> List[Dict]:
        """Fallback YouTube recommendations when API unavailable"""
        fallback_videos = {
            'joy': [
                {'title': 'Happy - Pharrell Williams (Official Video)', 'url': 'https://www.youtube.com/watch?v=ZbZSe6N_BXs', 'source': 'youtube'},
                {'title': 'Don\'t Stop Me Now - Queen', 'url': 'https://www.youtube.com/watch?v=HgzGwKwLmgM', 'source': 'youtube'},
            ],
            'anger': [
                {'title': '5-Minute Anger Management', 'url': 'https://www.youtube.com/watch?v=O5-1ywPHnGU', 'source': 'youtube'},
                {'title': 'Box Breathing Exercise', 'url': 'https://www.youtube.com/watch?v=H5iE8puj60k', 'source': 'youtube'},
            ],
            'sadness': [
                {'title': 'The Power of Vulnerability - Brené Brown', 'url': 'https://www.youtube.com/watch?v=iCv7Ml5CRtI', 'source': 'youtube'},
                {'title': 'Fix You - Coldplay (Official Video)', 'url': 'https://www.youtube.com/watch?v=k4V3Mo61fJM', 'source': 'youtube'},
            ],
            'fear': [
                {'title': '5-4-3-2-1 Grounding Technique', 'url': 'https://www.youtube.com/watch?v=Q1HH1qZzCqM', 'source': 'youtube'},
                {'title': '10 Minute Guided Meditation for Anxiety', 'url': 'https://www.youtube.com/watch?v=inpok4MKVLM', 'source': 'youtube'},
            ],
            'neutral': [
                {'title': 'Lo-Fi Beats to Study/Relax To', 'url': 'https://www.youtube.com/watch?v=jfKfPfyJRdk', 'source': 'youtube'},
                {'title': 'Peaceful Piano Music', 'url': 'https://www.youtube.com/watch?v=3jWRrafhO7M', 'source': 'youtube'},
            ]
        }

        videos = fallback_videos.get(emotion, fallback_videos['neutral'])
        for video in videos:
            video['emotion'] = emotion
            video['thumbnail'] = 'https://img.youtube.com/vi/default.jpg'

        return videos

    def get_spotify_playlists(self, emotion: str, context: str = "", limit: int = 5) -> List[Dict]:
        """
        Fetch music playlists (Spotify + Myanmar alternatives)

        Args:
            emotion: Detected emotion
            context: Additional context
            limit: Number of playlists

        Returns:
            List of playlist recommendations
        """
        # Spotify playlists (global)
        spotify_playlists = {
            'joy': [
                {'title': 'Happy Hits!', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC', 'description': 'Feel good pop hits', 'source': 'spotify'},
                {'title': 'Good Vibes', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4', 'description': 'Positive energy music', 'source': 'spotify'}
            ],
            'anger': [
                {'title': 'Peaceful Piano', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO', 'description': 'Calming piano pieces', 'source': 'spotify'},
                {'title': 'Deep Focus', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ', 'description': 'Focus and calm', 'source': 'spotify'}
            ],
            'sadness': [
                {'title': 'Sad Songs', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX3YSRoSdA634', 'description': 'Emotional comfort songs', 'source': 'spotify'},
                {'title': 'Comfort Songs', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX7K31D69s4M1', 'description': 'Songs that hug you back', 'source': 'spotify'}
            ],
            'fear': [
                {'title': 'Anxiety Relief', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWZqd5JICZI0u', 'description': 'Calming music for anxiety', 'source': 'spotify'},
                {'title': 'Meditation Music', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWZqd5JICZI0u', 'description': 'Peaceful meditation', 'source': 'spotify'}
            ],
            'neutral': [
                {'title': 'Lo-Fi Beats', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn', 'description': 'Chill lo-fi beats', 'source': 'spotify'},
                {'title': 'Peaceful Guitar', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX1n9whBbBKoL', 'description': 'Gentle guitar music', 'source': 'spotify'}
            ]
        }

        # Myanmar-specific music alternatives (YouTube Music, Facebook, local platforms)
        myanmar_music = {
            'joy': [
                {'title': 'Myanmar Happy Songs Playlist', 'url': 'https://www.youtube.com/results?search_query=myanmar+happy+songs', 'description': 'မြန်မာသီချင်းပျော်ရွှင်စရာများ', 'source': 'youtube_music'},
                {'title': 'Myanmar Pop Hits', 'url': 'https://www.youtube.com/results?search_query=myanmar+pop+songs+2024', 'description': 'နောက်ဆုံးထွက်မြန်မာပေါ့ပ်သီချင်းများ', 'source': 'youtube_music'},
                {'title': 'Myanmar Traditional Music', 'url': 'https://www.youtube.com/results?search_query=myanmar+traditional+music', 'description': 'မြန်မာ့ရိုးရာဂီတ', 'source': 'youtube_music'}
            ],
            'anger': [
                {'title': 'Calming Myanmar Songs', 'url': 'https://www.youtube.com/results?search_query=myanmar+calming+music', 'description': 'စိတ်ငြိမ်အေးစေသောသီချင်းများ', 'source': 'youtube_music'},
                {'title': 'Myanmar Acoustic', 'url': 'https://www.youtube.com/results?search_query=myanmar+acoustic+songs', 'description': 'အကောင်းစားသီချင်းများ', 'source': 'youtube_music'},
                {'title': 'Buddha Chanting', 'url': 'https://www.youtube.com/results?search_query=myanmar+buddha+chanting', 'description': 'တရားတော်နှင့်သီချင်းများ', 'source': 'youtube_music'}
            ],
            'sadness': [
                {'title': 'Myanmar Sad Songs', 'url': 'https://www.youtube.com/results?search_query=myanmar+sad+songs', 'description': 'မြန်မာသီချင်းစိတ်ဓာတ်ကျစရာများ', 'source': 'youtube_music'},
                {'title': 'Myanmar Ballads', 'url': 'https://www.youtube.com/results?search_query=myanmar+love+ballads', 'description': 'အချစ်သီချင်းများ', 'source': 'youtube_music'},
                {'title': 'Comfort Myanmar Songs', 'url': 'https://www.youtube.com/results?search_query=myanmar+comfort+songs', 'description': 'စိတ်သက်သာစေသောသီချင်းများ', 'source': 'youtube_music'}
            ],
            'fear': [
                {'title': 'Myanmar Meditation Music', 'url': 'https://www.youtube.com/results?search_query=myanmar+meditation+music', 'description': 'တရားထိုင်ဂီတ', 'source': 'youtube_music'},
                {'title': 'Myanmar Dhamma Talks', 'url': 'https://www.youtube.com/results?search_query=myanmar+dhamma+talks', 'description': 'တရားတော်များ', 'source': 'youtube_music'},
                {'title': 'Relaxing Myanmar Instrumental', 'url': 'https://www.youtube.com/results?search_query=myanmar+instrumental+music', 'description': 'တူရိယာဂီတ', 'source': 'youtube_music'}
            ],
            'neutral': [
                {'title': 'Myanmar Lo-Fi', 'url': 'https://www.youtube.com/results?search_query=myanmar+lofi+music', 'description': 'မြန်မာလိုဖိုင်းဂီတ', 'source': 'youtube_music'},
                {'title': 'Myanmar Chill Music', 'url': 'https://www.youtube.com/results?search_query=myanmar+chill+music', 'description': 'အနားယူဂီတ', 'source': 'youtube_music'},
                {'title': 'Myanmar Study Music', 'url': 'https://www.youtube.com/results?search_query=myanmar+study+music', 'description': 'စာကျက်ဂီတ', 'source': 'youtube_music'}
            ]
        }

        # Combine both sources
        emotion_spotify = spotify_playlists.get(emotion, spotify_playlists['neutral'])
        emotion_myanmar = myanmar_music.get(emotion, myanmar_music['neutral'])

        # Return based on limit (mix of both)
        combined = []
        for i in range(limit):
            if i < len(emotion_spotify):
                combined.append(emotion_spotify[i])
            if i < len(emotion_myanmar):
                combined.append(emotion_myanmar[i])

        for item in combined[:limit]:
            item['emotion'] = emotion

        return combined[:limit]

    def get_podcast_episodes(self, emotion: str, context: str = "", limit: int = 5) -> List[Dict]:
        """
        Fetch podcast episodes from iTunes API

        Args:
            emotion: Detected emotion
            context: Additional context
            limit: Number of episodes

        Returns:
            List of podcast episode recommendations
        """
        cache_key = self._generate_cache_key('podcast', emotion, limit)
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        queries = self.EMOTION_QUERIES.get(emotion, {}).get('podcast', ['mental health'])
        search_term = queries[0]

        try:
            params = {
                'term': search_term,
                'media': 'podcast',
                'limit': limit,
                'country': 'us'
            }

            response = self.session.get(self.ITUNES_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            episodes = []
            for item in data.get('results', [])[:limit]:
                episodes.append({
                    'title': item.get('collectionName', 'Unknown Podcast'),
                    'episode': item.get('trackName', 'Episode'),
                    'url': item.get('collectionViewUrl', ''),
                    'preview_url': item.get('previewUrl', ''),
                    'artist': item.get('artistName', 'Unknown'),
                    'thumbnail': item.get('artworkUrl100', ''),
                    'source': 'podcast',
                    'emotion': emotion
                })

            self._save_to_cache(cache_key, episodes)
            return episodes

        except Exception as e:
            print(f"Podcast API error: {e}")
            return self._get_fallback_podcasts(emotion)

    def _get_fallback_podcasts(self, emotion: str) -> List[Dict]:
        """Fallback podcast recommendations"""
        fallback = {
            'joy': [
                {'title': 'The Happiness Lab', 'episode': 'Finding Joy', 'url': 'https://www.happinesslab.fm/', 'source': 'podcast'},
                {'title': 'Ten Percent Happier', 'episode': 'Maintaining Positive Energy', 'url': 'https://www.tenpercent.com/', 'source': 'podcast'}
            ],
            'anger': [
                {'title': 'Ten Percent Happier', 'episode': 'Working with Anger', 'url': 'https://www.tenpercent.com/', 'source': 'podcast'},
                {'title': 'The Daily Stoic', 'episode': 'Controlling Your Reactions', 'url': 'https://dailystoic.com/', 'source': 'podcast'}
            ],
            'sadness': [
                {'title': 'Terrible, Thanks for Asking', 'episode': 'It\'s Okay to Not Be Okay', 'url': 'https://www.ttfa.org/', 'source': 'podcast'},
                {'title': 'The Hilarious World of Depression', 'episode': 'Finding Light', 'url': 'https://www.depressionpodcast.org/', 'source': 'podcast'}
            ],
            'fear': [
                {'title': 'The Anxiety Coaches Podcast', 'episode': 'Calming Panic', 'url': 'https://www.theanxietycoaches.com/', 'source': 'podcast'},
                {'title': 'Mindful in Minutes', 'episode': 'Grounding Techniques', 'url': 'https://www.mindfulinminutes.com/', 'source': 'podcast'}
            ],
            'neutral': [
                {'title': 'Stuff You Should Know', 'episode': 'Random Topics', 'url': 'https://www.stuffyoushouldknow.com/', 'source': 'podcast'},
                {'title': 'TED Radio Hour', 'episode': 'Ideas Worth Spreading', 'url': 'https://www.npr.org/podcasts/510307/ted-radio-hour', 'source': 'podcast'}
            ]
        }

        episodes = fallback.get(emotion, fallback['neutral'])
        for episode in episodes:
            episode['emotion'] = emotion

        return episodes

    def get_news_articles(self, emotion: str, context: str = "", limit: int = 5) -> List[Dict]:
        """
        Fetch news articles (International + Myanmar sources)

        Args:
            emotion: Detected emotion
            context: Additional context
            limit: Number of articles

        Returns:
            List of article recommendations
        """
        # Myanmar news sources (curated, no API required)
        myanmar_news = {
            'joy': [
                {'title': 'မြန်မာနိုင်ငံ ကောင်းသောသတင်းများ', 'url': 'https://www.facebook.com/myanmargoodnews', 'source': 'Facebook', 'description': 'Positive news from Myanmar'},
                {'title': 'Myanmar Success Stories', 'url': 'https://www.mmtimes.com/', 'source': 'Myanmar Times', 'description': 'Success stories and positive developments'},
                {'title': 'Myanmar Culture & Arts', 'url': 'https://www.gomymyanmar.com/', 'source': 'GoMyanmar', 'description': 'Cultural news and events'}
            ],
            'anger': [
                {'title': 'Peace Building in Myanmar', 'url': 'https://www.irrawaddy.com/', 'source': 'The Irrawaddy', 'description': 'Peace and reconciliation news'},
                {'title': 'Conflict Resolution News', 'url': 'https://www.mizzima.com/', 'source': 'Mizzima', 'description': 'Resolution and dialogue updates'},
                {'title': 'Mindfulness in Daily Life', 'url': 'https://www.buddhismtoday.com/', 'source': 'Buddhism Today', 'description': 'Buddhist perspective on anger management'}
            ],
            'sadness': [
                {'title': 'Mental Health Awareness Myanmar', 'url': 'https://www.myanmarmentalhealth.org/', 'source': 'MM Mental Health', 'description': 'Mental health resources and support'},
                {'title': 'Community Support Stories', 'url': 'https://www.facebook.com/myanmarhelpline', 'source': 'Myanmar Helpline', 'description': 'Support community news'},
                {'title': 'Hope Stories from Myanmar', 'url': 'https://www.dvb.no/', 'source': 'DVB', 'description': 'Inspiring stories of resilience'}
            ],
            'fear': [
                {'title': 'Safety Tips Myanmar', 'url': 'https://www.facebook.com/safetymyanmar', 'source': 'Safety Myanmar', 'description': 'Safety and security information'},
                {'title': 'Health & Wellness Myanmar', 'url': 'https://www.health.gov.mm/', 'source': 'Ministry of Health', 'description': 'Health advisories and tips'},
                {'title': 'Stress Management Guide', 'url': 'https://www.myanmarhealth.org/', 'source': 'Myanmar Health', 'description': 'Wellness and stress relief'}
            ],
            'neutral': [
                {'title': 'Myanmar Current Affairs', 'url': 'https://www.elevenmyanmar.com/', 'source': 'Eleven Media', 'description': 'Latest news and updates'},
                {'title': 'Myanmar Technology News', 'url': 'https://www.myanmarit.com/', 'source': 'Myanmar IT', 'description': 'Tech news and innovations'},
                {'title': 'Myanmar Education News', 'url': 'https://www.moe.gov.mm/', 'source': 'Ministry of Education', 'description': 'Education updates'}
            ]
        }

        # International news (fallback if API available)
        international_news = {
            'joy': [
                {'title': 'Good News Network', 'url': 'https://www.goodnewsnetwork.org/', 'source': 'GNN', 'description': 'Positive news from around the world'},
                {'title': 'Happy News', 'url': 'https://happynews.com/', 'source': 'Happy News', 'description': 'Uplifting stories'}
            ],
            'anger': [
                {'title': 'Mindful.org', 'url': 'https://www.mindful.org/', 'source': 'Mindful', 'description': 'Mindfulness and anger management'},
                {'title': 'Psychology Today - Anger', 'url': 'https://www.psychologytoday.com/us/basics/anger', 'source': 'Psychology Today', 'description': 'Expert advice on anger'}
            ],
            'sadness': [
                {'title': 'NIMH - Depression', 'url': 'https://www.nimh.nih.gov/health/topics/depression', 'source': 'NIMH', 'description': 'Medical information on depression'},
                {'title': 'Mental Health America', 'url': 'https://www.mhanational.org/', 'source': 'MHA', 'description': 'Mental health resources'}
            ],
            'fear': [
                {'title': 'Anxiety and Depression Association', 'url': 'https://adaa.org/', 'source': 'ADAA', 'description': 'Anxiety support and resources'},
                {'title': 'HelpGuide - Anxiety', 'url': 'https://www.helpguide.org/articles/anxiety/anxiety-attacks-and-anxiety-disorders.htm', 'source': 'HelpGuide', 'description': 'Self-help guides'}
            ],
            'neutral': [
                {'title': 'Science Daily', 'url': 'https://www.sciencedaily.com/', 'source': 'Science Daily', 'description': 'Latest science news'},
                {'title': 'TED Ideas', 'url': 'https://ideas.ted.com/', 'source': 'TED', 'description': 'Ideas worth spreading'}
            ]
        }

        # Combine Myanmar and international sources
        emotion_myanmar = myanmar_news.get(emotion, myanmar_news['neutral'])
        emotion_international = international_news.get(emotion, international_news['neutral'])

        # Mix both sources
        combined = []
        for i in range(limit):
            if i < len(emotion_myanmar):
                combined.append(emotion_myanmar[i])
            if i < len(emotion_international):
                combined.append(emotion_international[i])

        for article in combined[:limit]:
            article['emotion'] = emotion

        return combined[:limit]

    def _get_fallback_news(self, emotion: str) -> List[Dict]:
        """Fallback news/website recommendations"""
        fallback = {
            'joy': [
                {'title': 'The Science of Happiness', 'url': 'https://www.greatergood.berkeley.edu/topic/happiness/definition', 'source': 'Greater Good', 'description': 'Research-based happiness tips'},
                {'title': 'Positive Psychology', 'url': 'https://positivepsychology.com/', 'source': 'PP Website', 'description': 'Evidence-based wellbeing'}
            ],
            'anger': [
                {'title': 'Managing Anger', 'url': 'https://www.apa.org/topics/anger/control', 'source': 'APA', 'description': 'Psychologist\'s guide to anger'},
                {'title': 'Mindfulness for Anger', 'url': 'https://www.mindful.org/how-to-work-with-anger/', 'source': 'Mindful.org', 'description': 'Buddhist approach'}
            ],
            'sadness': [
                {'title': 'Understanding Depression', 'url': 'https://www.nimh.nih.gov/health/topics/depression', 'source': 'NIMH', 'description': 'Medical information'},
                {'title': 'Coping with Sadness', 'url': 'https://www.psychologytoday.com/us/basics/depression', 'source': 'Psychology Today', 'description': 'Expert advice'}
            ],
            'fear': [
                {'title': 'Anxiety and Depression', 'url': 'https://adaa.org/', 'source': 'ADAA', 'description': 'Anxiety support resources'},
                {'title': 'Managing Fear', 'url': 'https://www.helpguide.org/articles/anxiety/anxiety-attacks-and-anxiety-disorders.htm', 'source': 'HelpGuide', 'description': 'Self-help guide'}
            ],
            'neutral': [
                {'title': 'Science Daily', 'url': 'https://www.sciencedaily.com/', 'source': 'Science Daily', 'description': 'Latest science news'},
                {'title': 'TED Ideas', 'url': 'https://ideas.ted.com/', 'source': 'TED', 'description': 'Ideas worth spreading'}
            ]
        }

        articles = fallback.get(emotion, fallback['neutral'])
        for article in articles:
            article['emotion'] = emotion

        return articles

    def get_ted_talks(self, emotion: str, context: str = "", limit: int = 5) -> List[Dict]:
        """
        Fetch TED Talks (using curated list + web scraping if needed)

        Args:
            emotion: Detected emotion
            context: Additional context
            limit: Number of talks

        Returns:
            List of TED talk recommendations
        """
        # Curated TED talks by emotion
        talks = {
            'joy': [
                {'title': 'The Science of Happiness', 'speaker': 'Dan Gilbert', 'url': 'https://www.ted.com/talks/dan_gilbert_asks_why_are_we_happy', 'duration': '21 min', 'views': '5M+'},
                {'title': 'The Happy Secret to Better Work', 'speaker': 'Shawn Achor', 'url': 'https://www.ted.com/talks/shawn_achor_the_happy_secret_to_better_work', 'duration': '12 min', 'views': '25M+'},
                {'title': 'What Makes a Good Life?', 'speaker': 'Robert Waldinger', 'url': 'https://www.ted.com/talks/robert_waldinger_what_makes_a_good_life_lessons_from_the_longest_study_on_happiness', 'duration': '12 min', 'views': '40M+'}
            ],
            'anger': [
                {'title': 'The Power of Vulnerability', 'speaker': 'Brené Brown', 'url': 'https://www.ted.com/talks/brene_brown_the_power_of_vulnerability', 'duration': '20 min', 'views': '60M+'},
                {'title': 'How to Practice Emotional First Aid', 'speaker': 'Guy Winch', 'url': 'https://www.ted.com/talks/guy_winch_how_to_practice_emotional_first_aid', 'duration': '17 min', 'views': '7M+'},
                {'title': 'The Skill of Self Confidence', 'speaker': 'Dr. Ivan Joseph', 'url': 'https://www.ted.com/talks/dr_ivan_joseph_the_skill_of_self_confidence', 'duration': '13 min', 'views': '8M+'}
            ],
            'sadness': [
                {'title': 'The Power of Vulnerability', 'speaker': 'Brené Brown', 'url': 'https://www.ted.com/talks/brene_brown_the_power_of_vulnerability', 'duration': '20 min', 'views': '60M+'},
                {'title': 'Depression, the Secret We Share', 'speaker': 'Andrew Solomon', 'url': 'https://www.ted.com/talks/andrew_solomon_depression_the_secret_we_share', 'duration': '32 min', 'views': '3M+'},
                {'title': 'All It Takes Is 10 Mindful Minutes', 'speaker': 'Andy Puddicombe', 'url': 'https://www.ted.com/talks/andy_puddicombe_all_it_takes_is_10_mindful_minutes', 'duration': '9 min', 'views': '8M+'}
            ],
            'fear': [
                {'title': 'How to Make Stress Your Friend', 'speaker': 'Kelly McGonigal', 'url': 'https://www.ted.com/talks/kelly_mcgonigal_how_to_make_stress_your_friend', 'duration': '14 min', 'views': '25M+'},
                {'title': 'The Gift and Power of Emotional Courage', 'speaker': 'Susan David', 'url': 'https://www.ted.com/talks/susan_david_the_gift_and_power_of_emotional_courage', 'duration': '19 min', 'views': '5M+'},
                {'title': 'Inside the Mind of a Master Procrastinator', 'speaker': 'Tim Urban', 'url': 'https://www.ted.com/talks/tim_urban_inside_the_mind_of_a_master_procrastinator', 'duration': '14 min', 'views': '70M+'}
            ],
            'neutral': [
                {'title': 'Do Schools Kill Creativity?', 'speaker': 'Ken Robinson', 'url': 'https://www.ted.com/talks/ken_robinson_says_schools_kill_creativity', 'duration': '19 min', 'views': '70M+'},
                {'title': 'The Power of Believing You Can Improve', 'speaker': 'Carol Dweck', 'url': 'https://www.ted.com/talks/carol_dweck_the_power_of_believing_that_you_can_improve', 'duration': '10 min', 'views': '15M+'},
                {'title': 'How to Learn Anything... Fast', 'speaker': 'Josh Kaufman', 'url': 'https://www.ted.com/talks/josh_kaufman_the_first_20_hours_how_to_learn_anything_fast', 'duration': '19 min', 'views': '20M+'}
            ]
        }

        emotion_talks = talks.get(emotion, talks['neutral'])
        for talk in emotion_talks[:limit]:
            talk['source'] = 'ted'
            talk['emotion'] = emotion
            talk['thumbnail'] = f"https://pi.tedcdn.com/r/talkstar-photos.s3.amazonaws.com/uploads/{talk['speaker'].replace(' ', '_')}.jpg"

        return emotion_talks[:limit]

    def get_all_recommendations(self, emotion: str, context: str = "", 
                                sources: Optional[List[str]] = None,
                                limit_per_source: int = 3) -> Dict:
        """
        Get comprehensive recommendations from all external sources

        Args:
            emotion: Detected emotion
            context: Additional context
            sources: Optional list of specific sources to fetch
            limit_per_source: Number of items per source

        Returns:
            Dictionary with recommendations from all sources
        """
        if sources is None:
            sources = ['youtube', 'spotify', 'podcast', 'news', 'ted']

        recommendations = {
            'emotion': emotion,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }

        # Fetch from each source (can be parallelized for speed)
        if 'youtube' in sources:
            recommendations['sources']['youtube'] = self.get_youtube_videos(
                emotion, context, limit_per_source
            )

        if 'spotify' in sources:
            recommendations['sources']['spotify'] = self.get_spotify_playlists(
                emotion, context, limit_per_source
            )

        if 'podcast' in sources:
            recommendations['sources']['podcast'] = self.get_podcast_episodes(
                emotion, context, limit_per_source
            )

        if 'news' in sources:
            recommendations['sources']['news'] = self.get_news_articles(
                emotion, context, limit_per_source
            )

        if 'ted' in sources:
            recommendations['sources']['ted'] = self.get_ted_talks(
                emotion, context, limit_per_source
            )

        # Add quick recommendation (first item from each source)
        recommendations['quick_picks'] = {}
        for source, items in recommendations['sources'].items():
            if items:
                recommendations['quick_picks'][source] = items[0]

        return recommendations


# Singleton instance
_recommender = None


def get_external_recommender() -> ExternalResourceRecommender:
    """Get or create ExternalResourceRecommender singleton"""
    global _recommender
    if _recommender is None:
        _recommender = ExternalResourceRecommender()
    return _recommender


def get_external_recommendations(emotion: str, context: str = "", 
                                 sources: Optional[List[str]] = None) -> Dict:
    """
    Convenience function to get external recommendations

    Args:
        emotion: Detected emotion
        context: Additional context
        sources: Optional list of sources

    Returns:
        Dictionary with external recommendations
    """
    return get_external_recommender().get_all_recommendations(emotion, context, sources)


if __name__ == "__main__":
    # Test the external recommender
    import json

    recommender = get_external_recommender()

    print("=" * 70)
    print("External Resource Recommendation Test")
    print("=" * 70)

    for emotion in ['joy', 'anger', 'sadness', 'fear', 'neutral']:
        print(f"\n{'='*70}")
        print(f"EMOTION: {emotion.upper()}")
        print(f"{'='*70}")

        recs = recommender.get_all_recommendations(emotion, limit_per_source=2)

        print(f"\n📱 Quick Picks:")
        for source, item in recs['quick_picks'].items():
            print(f"  {source.upper()}: {item.get('title', 'N/A')}")
            print(f"    URL: {item.get('url', 'N/A')}")

        print(f"\n📊 Full Recommendations:")
        for source, items in recs['sources'].items():
            print(f"\n  {source.upper()} ({len(items)} items):")
            for item in items:
                print(f"    • {item.get('title', 'N/A')}")
                if 'duration' in item:
                    print(f"      Duration: {item['duration']}")
                print(f"      URL: {item.get('url', 'N/A')[:60]}...")
