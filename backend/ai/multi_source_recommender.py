"""
Multi-Source Recommendation Engine
Provides comprehensive recommendations across music, podcasts, videos, activities, and more
"""

from typing import Dict, List, Optional
import random


# ─────────────────────────────────────────────────────────────────────────────
# Myanmar Language Social Messages & Quick Actions
# ─────────────────────────────────────────────────────────────────────────────

MYANMAR_SOCIAL_MESSAGES: Dict[str, List[str]] = {
    'joy': [
        "ဒီ သတင်းကောင်းကို မိတ်ဆွေတစ်ဦးဦးနှင့် မျှဝေလိုက်ပါ 🌟",
        "ဒီ ပျော်ရွှင်မှုကို မိသားစုနှင့် ဝေမျှပါ 💛",
        "ကျေးဇူးတင်ကြောင်း တစ်ဦးဦးကို မက်ဆေ့ပို့လိုက်ပါ",
        "ဒီနေ့ ကံကောင်းမှုကို မနက်ဖြန်မှတ်တမ်းတင်ထားပါ 📝",
    ],
    'anger': [
        "အခုချိန် နည်းနည်းအနားယူပြီး နောက်မှ ပြန်ဆွေးနွေးပါ 🧘",
        "ဒေါသ ဖြေနိုင်ဖို့ လမ်းလျှောက်ထွက်ပါ 🚶",
        "မိတ်ဆွေကို 'ခဏနေပြီး ပြန်ဆွေးနွေးမယ်' လို့ ပြောပါ",
        "ခံစားချက်တွေကို စာနဲ့ ရေးချပြီး ဖြစ်ဖြစ်ပျက်ပျက် လုပ်ပါ",
    ],
    'sadness': [
        "'ဒီနေ့ ကျွန်တော်/ကျွန်မ ခက်ခဲနေတယ်၊ ဂရုစိုက်ပေးနိုင်မလား' ဆိုပြီး မိတ်ဆွေကို ဆက်သွယ်ပါ 💙",
        "ကြည်ကြည်ဖြူဖြူ ငိုချင်ရင် ငိုပါ၊ အဆင်ပြေပါတယ် 🌧️",
        "ချစ်ခင်ရသူတစ်ဦးကို ဖုန်းဆက်ပြောပါ",
        "မိသားစုနှင့် ဆုံပြီး ဝေမျှပါ",
    ],
    'fear': [
        "ကြောက်နေတာကို လူချစ်ရာတစ်ဦးကို ပွင့်ပွင့်လင်းလင်း ပြောပါ 🤝",
        "'ကျွန်တော်/ကျွန်မ ပူပန်နေတယ်' ဆိုပြီး မိတ်ဆွေကို ပြောပါ",
        "ယုံကြည်ရသူတစ်ဦးနှင့် တွေ့ဆုံပါ",
        "အကူအညီတောင်းဖို့ မရှက်ပါနှင့် 💪",
    ],
    'neutral': [
        "မိတ်ဆွေတစ်ဦးကို 'ဘယ်လိုနေသလဲ' ဆိုပြီး ဆက်သွယ်ပါ",
        "ကောင်းကောင်းလေး မနက်ပြန်တွေ့ကြမယ် 😊",
        "ဒီနေ့ တစ်ခုခုကောင်းကောင်း လုပ်ဆောင်ဖို့ plan ချပါ",
    ],
}

MYANMAR_QUICK_ACTIONS: Dict[str, Dict] = {
    'joy': {
        'title': 'ဂျာနယ်ရေးပါ',
        'description': 'ဒီနေ့ ပျော်ရွှင်မှုကို ဂျာနယ်တွင် မှတ်တမ်းတင်ပါ',
        'duration': '5-10 မိနစ်',
        'effort': 'နည်း',
    },
    'anger': {
        'title': 'Box Breathing လေ့ကျင့်ပါ',
        'description': '4 ချက် ရှူသွင်း၊ 4 ချက် ကိုင်ထား၊ 4 ချက် ရှူထုတ် — 3 ကြိမ် ပြုလုပ်ပါ',
        'duration': '3-5 မိနစ်',
        'effort': 'နည်း',
    },
    'sadness': {
        'title': 'နွေးနွေးထွေးထွေး ဖျော်ရည်သောက်ပါ',
        'description': 'လက်ဖက်ရည် သို့မဟုတ် ကော်ဖီ တစ်ခွက် ၊ ကိုယ်ကို ဂရုစိုက်ပါ',
        'duration': '10-15 မိနစ်',
        'effort': 'နည်း',
    },
    'fear': {
        'title': '5-4-3-2-1 Grounding လုပ်ပါ',
        'description': 'မြင်ရတဲ့ 5 ခု၊ ထိနိုင်တဲ့ 4 ခု၊ ကြားရတဲ့ 3 ခု၊ မှုတ်ရတဲ့ 2 ခု၊ အရသာ 1 ခု — ပြောပါ',
        'duration': '3-5 မိနစ်',
        'effort': 'နည်း',
    },
    'neutral': {
        'title': 'လမ်းလျှောက်ထွက်ပါ',
        'description': 'ပတ်ဝန်းကျင်ကို သတိပြုရင်း တိတ်ဆိတ်စွာ လမ်းလျှောက်ပါ',
        'duration': '15-20 မိနစ်',
        'effort': 'နည်း',
    },
}


class MultiSourceRecommender:
    """Generate multi-source recommendations based on emotion"""

    # Comprehensive emotion-specific recommendations across multiple sources
    RECOMMENDATIONS = {
        'joy': {
            'music': [
                {"title": "Happy - Pharrell Williams", "type": "song", "description": "Upbeat pop anthem"},
                {"title": "Don't Stop Me Now - Queen", "type": "song", "description": "Energetic rock classic"},
                {"title": "Walking on Sunshine - Katrina and the Waves", "type": "song", "description": "Feel-good hit"},
                {"title": "Good as Hell - Lizzo", "type": "song", "description": "Empowering pop"},
                {"title": "Three Little Birds - Bob Marley", "type": "song", "description": "Relaxing reggae vibes"},
                {"title": "Can't Stop the Feeling! - Justin Timberlake", "type": "song", "description": "Dance-pop feel-good song"},
                {"title": "Lovely Day - Bill Withers", "type": "song", "description": "Smooth soulful classic"},
                {"title": "Best Day Of My Life - American Authors", "type": "song", "description": "Indie pop upbeat song"},
                {"title": "ဒီနေ့ - ထူးအိမ်သင်", "type": "song", "description": "Classic Myanmar upbeat song"},
                {"title": "ပျော်နေပါ - ဖြိုးမြတ်အောင်", "type": "song", "description": "Cheerful modern Myanmar pop"},
                {"title": "အောင်မြင်ခြင်းရဲ့နိဒါန်း - သားငယ်", "type": "song", "description": "Inspirational Myanmar song"}
            ],
            'podcast': [
                {"title": "The Happiness Lab", "episode": "Season 1: Finding Joy", "description": "Science of happiness"},
                {"title": "Ten Percent Happier", "episode": "Maintaining Positive Energy", "description": "Meditation & joy"},
                {"title": "Optimal Living Daily", "episode": "Celebrating Small Wins", "description": "Personal development"},
                {"title": "The Good Life Project", "episode": "Living with Purpose", "description": "Inspiring life stories"},
                {"title": "Daily Joy", "episode": "Finding Bliss in Small Things", "description": "Quick daily inspiration"}
            ],
            'video': [
                {"title": "The Science of Happiness", "platform": "TED Talk", "duration": "12 min", "description": "Research-backed tips"},
                {"title": "Happy - Official Music Video", "platform": "YouTube", "duration": "4 min", "description": "Feel-good visuals"},
                {"title": "Good News Compilation", "platform": "YouTube", "duration": "10 min", "description": "Positive news stories"},
                {"title": "မြန်မာနိုင်ငံ၏ လှပသော သဘာဝရှုခင်းများ", "platform": "YouTube", "duration": "10 min", "description": "Scenic Myanmar nature visuals"},
                {"title": "ကလေးငယ်တွေရဲ့ ပျော်ရွှင်စရာ ဟာသများ", "platform": "YouTube", "duration": "5 min", "description": "Funny kids compilation"}
            ],
            'activity': [
                {"title": "Dance Party", "description": "Put on your favorite upbeat songs and dance!", "duration": "10-15 min", "effort": "low"},
                {"title": "Gratitude Journaling", "description": "Write down 3 things you're grateful for", "duration": "5-10 min", "effort": "low"},
                {"title": "Share Your Joy", "description": "Call or message someone to share your happiness", "duration": "5-20 min", "effort": "low"},
                {"title": "Creative Expression", "description": "Draw, paint, or create something inspired by your mood", "duration": "20-30 min", "effort": "medium"},
                {"title": "Nature Walk", "description": "Take a walk outside and enjoy the moment", "duration": "15-30 min", "effort": "medium"},
                {"title": "လက်ဖက်ရည်ဆိုင်သွားပါ", "description": "မိတ်ဆွေတွေနဲ့အတူ လက်ဖက်ရည်ဆိုင်မှာ အချိန်ပေးပါ", "duration": "30-60 min", "effort": "low"}
            ],
            'book': [
                {"title": "The Happiness Project", "author": "Gretchen Rubin", "description": "Year-long happiness journey"},
                {"title": "Atomic Habits", "author": "James Clear", "description": "Building positive habits"},
                {"title": "The Power of Now", "author": "Eckhart Tolle", "description": "Living in the present"}
            ],
            'app': [
                {"name": "Headspace", "description": "Guided meditation for maintaining calm joy", "category": "Meditation"},
                {"name": "Daylio", "description": "Mood tracking to remember happy moments", "category": "Journal"},
                {"name": "Gratitude", "description": "Daily gratitude practice", "category": "Wellness"}
            ],
            'social': [
                "ဒီနေ့ တော်တော် ပျော်နေတာ၊ မင်းကိုလည်း ပျော်စေချင်လို့ ဒီသီချင်းလေး နားထောင်ကြည့်ပါဦး",
                "မင်းနဲ့ စကားပြောရတာ ငါ့အတွက် အမြဲတမ်း ပျော်ရွှင်စရာပဲ",
                "ကိုယ်တို့ ဒီနေ့ တစ်နေရာရာ သွားကြမလား? ကိုယ် တော်တော် စိတ်ကြည်လင်နေလို့",
                "Share your happiness on social media to inspire others",
                "Invite a friend for coffee or lunch to spread the joy",
                "Send a voice note of you laughing to a close friend"
            ],
            'self_care': [
                "Take a celebratory bubble bath with your favorite scent",
                "Treat yourself to your favorite dessert or a nice meal",
                "ဘုရားသွားပြီး စိတ်အေးချမ်းမှု ယူပါ",
                "ကိုယ်နှစ်သက်တဲ့ အဝတ်အစားလေးဝတ်ပြီး ယုံကြည်မှု တည်ဆောက်ပါ",
                "အသားအရေ ထိန်းသိမ်းတဲ့ (Skincare) အချိန်လေး ယူပါ",
                "မှန်ထဲကြည့်ပြီး ကိုယ့်ကိုယ်ကိုယ် ပြုံးပြပါ"
            ],
            'activity': [
                {"title": "Dance Party", "description": "Put on your favorite upbeat songs and dance!", "duration": "5-10 min", "effort": "medium"},
                {"title": "Gratitude Journaling", "description": "Write down 3 things you're grateful for", "duration": "10-15 min", "effort": "low"},
                {"title": "Creative Expression", "description": "Draw or paint something colorful", "duration": "20-30 min", "effort": "medium"},
                {"title": "လက်ဖက်ရည်ဆိုင်သွားပါ", "description": "သူငယ်ချင်းတွေနဲ့ စကားပြောရင်း အချိန်ကုန်ဆုံးပါ", "duration": "30-60 min", "effort": "low"},
                {"title": "ပန်းခြံထဲမှာ လမ်းလျှောက်ပါ", "description": "သဘာဝအလှကို ခံစားရင်း လန်းဆန်းမှုယူပါ", "duration": "15-20 min", "effort": "low"},
                {"title": "ဝါသနာပါရာ လုပ်ဆောင်ပါ", "description": "ကိုယ်ဝါသနာပါတဲ့ အလုပ်တစ်ခုကို အာရုံစိုက်လုပ်ပါ", "duration": "30-60 min", "effort": "medium"}
            ]
        },

        'anger': {
            'music': [
                {"title": "Weightless - Marconi Union", "type": "song", "description": "Scientifically designed to reduce stress"},
                {"title": "Clair de Lune - Debussy", "type": "classical", "description": "Calming piano piece"},
                {"title": "Watermark - Enya", "type": "new age", "description": "Soothing ambient sounds"},
                {"title": "Gymnopédie No.1 - Satie", "type": "classical", "description": "Peaceful piano composition"},
                {"title": "Breathe Me - Sia", "type": "song", "description": "Emotional release"},
                {"title": "အေးချမ်းပါစေ - မေခလာ", "type": "song", "description": "Soothing classic Myanmar song"},
                {"title": "တိတ်ဆိတ်ခြင်း - လင်းလင်း", "type": "song", "description": "Reflective Myanmar rock ballad"}
            ],
            'podcast': [
                {"title": "Ten Percent Happier", "episode": "Working with Anger", "description": "Buddhist perspective on anger"},
                {"title": "The Daily Stoic", "episode": "Controlling Your Reactions", "description": "Stoic wisdom"},
                {"title": "Mindful in Minutes", "episode": "Cooling Down Anger", "description": "Quick meditation"},
                {"title": "The Anger Management Podcast", "episode": "Coping Strategies", "description": "Expert advice"},
                {"title": "Buddhist Society Podcast", "episode": "Patience and Loving Kindness", "description": "Overcoming anger"}
            ],
            'video': [
                {"title": "Managing Anger", "platform": "TED Talk", "duration": "15 min", "description": "Psychologist's guide"},
                {"title": "5-Minute Anger Management", "platform": "YouTube", "duration": "5 min", "description": "Quick techniques"},
                {"title": "Box Breathing Exercise", "platform": "YouTube", "duration": "4 min", "description": "Calming breathing"},
                {"title": "ငြိမ်းချမ်းစွာ နေထိုင်ခြင်း - ဆရာတော် ဦးဇောတိက", "platform": "YouTube", "duration": "20 min", "description": "Dhamma talk on peace"}
            ],
            'activity': [
                {"title": "Box Breathing", "description": "Inhale 4s, hold 4s, exhale 4s, hold 4s", "duration": "3-5 min", "effort": "low"},
                {"title": "Progressive Muscle Relaxation", "description": "Tense and release each muscle group", "duration": "10-15 min", "effort": "low"},
                {"title": "Write & Release", "description": "Write your feelings, then tear it up", "duration": "10 min", "effort": "low"},
                {"title": "Cold Water Splash", "description": "Splash cold water on your face", "duration": "1-2 min", "effort": "low"},
                {"title": "Walk It Off", "description": "Take a brisk walk to release tension", "duration": "15-20 min", "effort": "medium"},
                {"title": "Punch Pillow", "description": "Physical release in a safe way", "duration": "2-5 min", "effort": "medium"},
                {"title": "ရေအေးအေးလေး သောက်ပါ", "description": "စိတ်အေးသွားအောင် ရေအေးအေးတစ်ခွက် သောက်လိုက်ပါ", "duration": "2 min", "effort": "low"}
            ],
            'book': [
                {"title": "Anger: Wisdom for Cooling the Flames", "author": "Thich Nhat Hanh", "description": "Buddhist approach to anger"},
                {"title": "The Dance of Anger", "author": "Harriet Lerner", "description": "Understanding anger patterns"},
                {"title": "Rage", "author": "Octavio Paz", "description": "Poetic exploration of anger"}
            ],
            'app': [
                {"name": "Calm", "description": "Guided meditations for anger management", "category": "Meditation"},
                {"name": "Sanvello", "description": "Mood tracking and coping tools", "category": "Mental Health"},
                {"name": "Breathe2Relax", "description": "Breathing exercises", "category": "Stress Relief"}
            ],
            'social': [
                "စိတ်မဆိုးပါနဲ့တော့နော်၊ နောက်ဆို ဒါမျိုး မဖြစ်စေရဘူးလို့ ကတိပေးပါတယ်",
                "အခု ကိုယ် နည်းနည်း စိတ်တိုနေလို့ ခဏနေမှ ပြန်ပြောကြရအောင်နော်",
                "ကိုယ့်ဘက်က မှားသွားတာရှိရင် တောင်းပန်ပါတယ်၊ အေးအေးဆေးဆေး စကားပြောချင်လို့ပါ",
                "I'm feeling a bit overwhelmed right now, can we talk in 10 minutes?",
                "I apologize for my earlier reaction, I was stressed."
            ],
            'self_care': [
                "ဒေါသထွက်လာလျှင် ၁ မှ ၁၀ အထိ စိတ်ထဲမှ ဖြည်းဖြည်းချင်း ရေတွက်ပါ",
                "လက်ရှိနေရာမှ ခေတ္တဖယ်ခွာပြီး ရေအေးအေးတစ်ခွက် သောက်လိုက်ပါ",
                "မျက်လုံးမှိတ်ပြီး စိတ်အေးချမ်းမည့် နေရာတစ်ခုကို စိတ်ကူးယဉ်ပါ",
                "Write your anger down on paper and then rip it up",
                "Listen to heavy metal or high-energy music to release tension"
            ]
        },

        'sadness': {
            'music': [
                {"title": "Lean on Me - Bill Withers", "type": "song", "description": "Comforting soul classic"},
                {"title": "Bridge Over Troubled Water - Simon & Garfunkel", "type": "song", "description": "Supportive folk"},
                {"title": "Rainbow - Kacey Musgraves", "type": "song", "description": "Hopeful country"},
                {"title": "Fix You - Coldplay", "type": "song", "description": "Emotional healing"},
                {"title": "Here Comes the Sun - The Beatles", "type": "song", "description": "Hopeful classic"},
                {"title": "အလွမ်းပြေ - ထူးအိမ်သင်", "type": "song", "description": "Reflective Myanmar classic"},
                {"title": "နေပါစေ - စိုင်းစိုင်းခမ်းလှိုင်", "type": "song", "description": "Melancholic Myanmar pop"}
            ],
            'podcast': [
                {"title": "The Sad, Sad Podcast", "episode": "Processing Grief", "description": "Mental health discussions"},
                {"title": "Terrible, Thanks for Asking", "episode": "It's Okay to Not Be Okay", "description": "Honest conversations"},
                {"title": "The Hilarious World of Depression", "episode": "Finding Light", "description": "Comedy meets depression"},
                {"title": "Meditation Minis", "episode": "Lifting the Cloud", "description": "Short meditations for sadness"},
                {"title": "The Overwhelmed Brain", "episode": "Processing Deep Emotions", "description": "Emotional intelligence"}
            ],
            'video': [
                {"title": "The Power of Vulnerability", "platform": "TED Talk", "duration": "20 min", "description": "Brené Brown's classic"},
                {"title": "Depression is an Illness", "platform": "YouTube", "duration": "8 min", "description": "Understanding sadness"},
                {"title": "Comforting Rain Sounds", "platform": "YouTube", "duration": "1 hour", "description": "Calming background"},
                {"title": "အားတင်းထားပါ - စိတ်ခွန်အားဖြည့် ဗီဒီယို", "platform": "YouTube", "duration": "8 min", "description": "Motivational Myanmar video"},
                {"title": "Funny Animal Compilation", "platform": "YouTube", "duration": "10 min", "description": "Laughter is the best medicine"}
            ],
            'activity': [
                {"title": "Warm Beverage Ritual", "description": "Make tea or hot chocolate mindfully", "duration": "10-15 min", "effort": "low"},
                {"title": "Comfort Movie", "description": "Watch a favorite feel-good film", "duration": "1.5-2 hours", "effort": "low"},
                {"title": "Gentle Stretching", "description": "Light yoga or stretching", "duration": "10-15 min", "effort": "low"},
                {"title": "Call a Loved One", "description": "Reach out to someone who cares", "duration": "15-30 min", "effort": "medium"},
                {"title": "Self-Compassion Letter", "description": "Write yourself a kind letter", "duration": "15-20 min", "effort": "medium"},
                {"title": "Cozy Blanket Time", "description": "Wrap up and rest without guilt", "duration": "30-60 min", "effort": "low"},
                {"title": "အလှူလေး တစ်ခုခု လုပ်ပါ", "description": "စိတ်ချမ်းသာအောင် တတ်နိုင်သလောက် အလှူဒါန လုပ်ပါ", "duration": "10-30 min", "effort": "low"}
            ],
            'book': [
                {"title": "The Noonday Demon", "author": "Andrew Solomon", "description": "Anatomy of depression"},
                {"title": "Reasons to Stay Alive", "author": "Matt Haig", "description": "Memoir of surviving depression"},
                {"title": "The Upward Spiral", "author": "Alex Korb", "description": "Neuroscience of depression"},
                {"title": "Feeling Good", "author": "David Burns", "description": "Cognitive Behavioral Therapy basics"},
                {"title": "Man's Search for Meaning", "author": "Viktor Frankl", "description": "Finding hope in suffering"}
            ],
            'app': [
                {"name": "Woebot", "description": "AI therapy chatbot for support", "category": "Mental Health"},
                {"name": "Moodpath", "description": "Depression screening and tracking", "category": "Mental Health"},
                {"name": "Insight Timer", "description": "Free meditation library", "category": "Meditation"},
                {"name": "Happify", "description": "Science-based activities for happiness", "category": "Wellness"},
                {"name": "Sanvello", "description": "Coping tools for depression", "category": "Mental Health"}
            ],
            'social': [
                "အခုတလော ကိုယ် စိတ်မကောင်းဖြစ်နေလို့ မင်းရဲ့အားပေးစကားလေးတွေ လိုချင်တယ်",
                "ကိုယ့်နားမှာ ရှိပေးရုံနဲ့တင် ကိုယ် တော်တော် အားရှိပါတယ်",
                "အရာအားလုံး အဆင်ပြေသွားမှာပါနော်၊ ကိုယ်တို့ အတူတူ ကျော်ဖြတ်ကြမယ်",
                "I'm feeling a bit down today, would love to hear your voice.",
                "Thank you for being there for me, it means a lot."
            ],
            'self_care': [
                "စိတ်ညစ်စရာရှိရင် တစ်ယောက်ယောက်ကို ရင်ဖွင့်ပြောပြလိုက်ပါ",
                "မျက်ရည်ကျချင်ရင်လည်း အောင့်မထားဘဲ ငိုချပစ်လိုက်ပါ",
                "နွေးနွေးထွေးထွေးရှိမည့် အစားအစာတစ်ခုခု စားပါ",
                "Take a warm shower and wear comfortable clothes",
                "Listen to your favorite sad songs to process the feeling"
            ]
        },

        'fear': {
            'music': [
                {"title": "Brave - Sara Bareilles", "type": "song", "description": "Empowering pop anthem"},
                {"title": "Eye of the Tiger - Survivor", "type": "song", "description": "Motivational rock"},
                {"title": "Unwritten - Natasha Bedingfield", "type": "song", "description": "Hopeful pop"},
                {"title": "Titanium - David Guetta ft. Sia", "type": "song", "description": "Strong EDM anthem"},
                {"title": "A Thousand Years - Christina Perri", "type": "song", "description": "Calming ballad"},
                {"title": "အမှောင်ထဲက လက်တစ်ကမ်း - ဇော်ဝင်းထွဋ်", "type": "song", "description": "Courageous Myanmar rock"},
                {"title": "အားတင်းထား - မျိုးကြီး", "type": "song", "description": "Motivational Myanmar rock"}
            ],
            'podcast': [
                {"title": "Fearless", "episode": "Overcoming Anxiety", "description": "Practical strategies"},
                {"title": "The Anxiety Coaches Podcast", "episode": "Calming Panic", "description": "Expert advice"},
                {"title": "Mindful in Minutes", "episode": "Grounding Techniques", "description": "Quick anxiety relief"}
            ],
            'video': [
                {"title": "All It Takes Is 10 Mindful Minutes", "platform": "TED Talk", "duration": "10 min", "description": "Andy Puddicombe"},
                {"title": "5-4-3-2-1 Grounding Technique", "platform": "YouTube", "duration": "5 min", "description": "Anxiety relief"},
                {"title": "Progressive Muscle Relaxation", "platform": "YouTube", "duration": "15 min", "description": "Full body relaxation"},
                {"title": "ကြောက်စိတ်ကို ဘယ်လိုကျော်လွှားမလဲ - Motivation", "platform": "YouTube", "duration": "12 min", "description": "Myanmar guide to courage"}
            ],
            'activity': [
                {"title": "5-4-3-2-1 Grounding", "description": "Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste", "duration": "3-5 min", "effort": "low"},
                {"title": "Power Posing", "description": "Stand tall in a confident pose for 2 minutes", "duration": "2 min", "effort": "low"},
                {"title": "Worry Time", "description": "Schedule 15 min to worry, then move on", "duration": "15 min", "effort": "low"},
                {"title": "Fact-Check Your Fears", "description": "Write down what you fear vs. what's likely", "duration": "10-15 min", "effort": "medium"},
                {"title": "Call Your Support Person", "description": "Talk to someone who makes you feel safe", "duration": "15-30 min", "effort": "medium"},
                {"title": "Visualization Exercise", "description": "Imagine your safe place in detail", "duration": "10 min", "effort": "low"},
                {"title": "ယုံကြည်ရသူ တစ်ဦးကို ရင်ဖွင့်ပါ", "description": "ကိုယ့်ရဲ့ စိုးရိမ်မှုကို တစ်ယောက်ယောက်ကို ပြောပြပါ", "duration": "15-30 min", "effort": "medium"}
            ],
            'book': [
                {"title": "Dare", "author": "Barry McDonagh", "description": "Anxiety and panic relief"},
                {"title": "The Anxiety and Phobia Workbook", "author": "Edmund Bourne", "description": "Practical exercises"},
                {"title": "Feel the Fear and Do It Anyway", "author": "Susan Jeffers", "description": "Classic self-help"},
                {"title": "My Age of Anxiety", "author": "Scott Stossel", "description": "Fear and anxiety through history"},
                {"title": "The Gift of Fear", "author": "Gavin de Becker", "description": "Understanding intuition and safety"}
            ],
            'app': [
                {"name": "Dare", "description": "Anxiety and panic attack relief", "category": "Mental Health"},
                {"name": "Rootd", "description": "Panic attack & anxiety relief", "category": "Mental Health"},
                {"name": "Finch", "description": "Self-care pet game for mental health", "category": "Wellness"},
                {"name": "Mindshift CBT", "description": "CBT tools for anxiety", "category": "Mental Health"},
                {"name": "Worry Watch", "description": "Anxiety and worry tracking", "category": "Wellness"}
            ],
            'social': [
                "Tell someone: 'I'm feeling anxious, can you help me talk through it?'",
                "Join an anxiety support community",
                "Schedule a therapy appointment",
                "Ask a friend to accompany you to a stressful event"
            ],
            'self_care': [
                "Create a safety kit with comforting items",
                "Practice deep breathing with extended exhales",
                "Use calming essential oils (lavender, bergamot)",
                "Wrap yourself in a weighted blanket"
            ]
        },

        'neutral': {
            'music': [
                {"title": "Lo-Fi Beats Playlist", "type": "playlist", "description": "Chill background music"},
                {"title": "Peaceful Piano - Spotify", "type": "playlist", "description": "Relaxing instrumentals"},
                {"title": "Coffee Shop Jazz", "type": "playlist", "description": "Smooth jazz vibes"},
                {"title": "Nature Sounds Mix", "type": "ambient", "description": "Calming natural sounds"},
                {"title": "Acoustic Morning - Playlist", "type": "playlist", "description": "Gentle acoustic songs"}
            ],
            'podcast': [
                {"title": "Stuff You Should Know", "episode": "Random Interesting Topics", "description": "Educational fun"},
                {"title": "TED Radio Hour", "episode": "Ideas Worth Spreading", "description": "Inspiring talks"},
                {"title": "The Daily", "episode": "Current Events", "description": "News roundup"}
            ],
            'video': [
                {"title": "Try Not to Smile Challenge", "platform": "YouTube", "duration": "10 min", "description": "Light entertainment"},
                {"title": "How to Build Better Habits", "platform": "TED Talk", "duration": "15 min", "description": "Self-improvement"},
                {"title": "Amazing Nature Documentary Clips", "platform": "YouTube", "duration": "20 min", "description": "Relaxing visuals"}
            ],
            'activity': [
                {"title": "Learn Something New", "description": "Watch a tutorial or read about a topic", "duration": "20-30 min", "effort": "medium"},
                {"title": "Organize One Small Thing", "description": "Tidy your desk or a drawer", "duration": "10-15 min", "effort": "low"},
                {"title": "Take a Mindful Walk", "description": "Notice your surroundings without judgment", "duration": "15-20 min", "effort": "low"},
                {"title": "Try a New Recipe", "description": "Cook something you've never made before", "duration": "30-60 min", "effort": "medium"},
                {"title": "Stretch Break", "description": "Do some light stretching", "duration": "5-10 min", "effort": "low"},
                {"title": "Plan Something Fun", "description": "Schedule an activity to look forward to", "duration": "10 min", "effort": "low"}
            ],
            'book': [
                {"title": "Atomic Habits", "author": "James Clear", "description": "Small changes, big results"},
                {"title": "Sapiens", "author": "Yuval Noah Harari", "description": "Fascinating history"},
                {"title": "The Alchemist", "author": "Paulo Coelho", "description": "Inspiring fiction"}
            ],
            'app': [
                {"name": "Duolingo", "description": "Learn a language in spare moments", "category": "Education"},
                {"name": "Blinkist", "description": "Book summaries in 15 minutes", "category": "Education"},
                {"name": "Streaks", "description": "Build positive habits", "category": "Productivity"}
            ],
            'social': [
                "Send a 'thinking of you' message to a friend",
                "Comment positively on someone's post",
                "Schedule a catch-up call",
                "Join an online community around your interests"
            ],
            'self_care': [
                "Drink a full glass of water",
                "Step outside for fresh air",
                "Do a quick body scan meditation",
                "Apply hand cream or lotion mindfully"
            ]
        }
    }

    def get_recommendations(self, emotion: str, context: str = "",
                           source_types: Optional[List[str]] = None,
                           count: int = 4, language: str = 'en') -> Dict:
        """
        Get multi-source recommendations based on emotion

        Args:
            emotion: Detected emotion (joy, anger, sadness, fear, neutral)
            context: Optional context text (for future enhancement)
            source_types: Optional list of specific source types to include
            count: Number of recommendations per source type

        Returns:
            Dictionary with recommendations from multiple sources
        """
        # Get all recommendations for this emotion
        emotion_recs = self.RECOMMENDATIONS.get(emotion, self.RECOMMENDATIONS['neutral'])

        # Default source types
        if source_types is None:
            source_types = ['music', 'podcast', 'video', 'activity', 'self_care']

        # Build response
        recommendations = {
            'emotion': emotion,
            'sources': {}
        }

        for source_type in source_types:
            if source_type in emotion_recs:
                items = emotion_recs[source_type]
                # Select random items if more available than count
                if len(items) > count:
                    selected = random.sample(items, count)
                else:
                    selected = items
                recommendations['sources'][source_type] = selected

        # Add quick action (single immediate recommendation)
        if 'activity' in emotion_recs:
            recommendations['quick_action'] = random.choice(emotion_recs['activity'])

        # Add send_message suggestion — Myanmar or English based on language
        if language == 'my':
            my_msgs = MYANMAR_SOCIAL_MESSAGES.get(emotion, MYANMAR_SOCIAL_MESSAGES['neutral'])
            recommendations['send_message'] = random.choice(my_msgs)
            recommendations['quick_action'] = MYANMAR_QUICK_ACTIONS.get(
                emotion, MYANMAR_QUICK_ACTIONS['neutral']
            )
        else:
            if 'social' in emotion_recs:
                recommendations['send_message'] = random.choice(emotion_recs['social'])

        return recommendations

    def get_quick_recommendation(self, emotion: str) -> Dict:
        """Get a single quick recommendation"""
        emotion_recs = self.RECOMMENDATIONS.get(emotion, self.RECOMMENDATIONS['neutral'])

        # Prioritize activities for quick action
        if 'activity' in emotion_recs:
            activity = random.choice(emotion_recs['activity'])
            return {
                'type': 'activity',
                'title': activity['title'],
                'description': activity['description'],
                'duration': activity.get('duration', '5-10 min'),
                'emotion': emotion
            }

        return {'type': 'none', 'emotion': emotion}

    def get_all_sources(self) -> List[str]:
        """Get list of all available source types"""
        return ['music', 'podcast', 'video', 'activity', 'book', 'app', 'social', 'self_care']

    def get_emotion_sources(self, emotion: str) -> List[str]:
        """Get available source types for a specific emotion"""
        emotion_recs = self.RECOMMENDATIONS.get(emotion, self.RECOMMENDATIONS['neutral'])
        return list(emotion_recs.keys())


# Singleton instance
_recommender = None


def get_recommender() -> MultiSourceRecommender:
    """Get or create MultiSourceRecommender singleton"""
    global _recommender
    if _recommender is None:
        _recommender = MultiSourceRecommender()
    return _recommender


def get_recommendations(emotion: str, context: str = "",
                       source_types: Optional[List[str]] = None,
                       language: str = 'en') -> Dict:
    """
    Convenience function to get multi-source recommendations

    Args:
        emotion: Detected emotion
        context: Optional context
        source_types: Optional list of source types
        language: 'en' for English, 'my' for Myanmar

    Returns:
        Multi-source recommendation dictionary
    """
    return get_recommender().get_recommendations(emotion, context, source_types, language=language)


def get_quick_recommendation(emotion: str) -> Dict:
    """Get a single quick recommendation"""
    return get_recommender().get_quick_recommendation(emotion)


if __name__ == "__main__":
    import json

    # Test the recommender
    recommender = MultiSourceRecommender()

    print("=" * 70)
    print("Multi-Source Recommendation Engine Test")
    print("=" * 70)

    for emotion in ['joy', 'anger', 'sadness', 'fear', 'neutral']:
        print(f"\n{'='*70}")
        print(f"EMOTION: {emotion.upper()}")
        print(f"{'='*70}")

        recs = recommender.get_recommendations(emotion, count=2)

        print(f"\n📱 Quick Action: {recs['quick_action']['title']}")
        print(f"   {recs['quick_action']['description']}")

        print(f"\n💬 Social: {recs['send_message']}")

        for source_type, items in recs['sources'].items():
            print(f"\n{source_type.upper()}:")
            for item in items:
                if source_type == 'music':
                    print(f"  🎵 {item['title']} - {item['description']}")
                elif source_type == 'podcast':
                    print(f"  🎧 {item['title']}: {item['episode']}")
                    print(f"     {item['description']}")
                elif source_type == 'video':
                    print(f"  📺 {item['title']} ({item['platform']}, {item['duration']})")
                    print(f"     {item['description']}")
                elif source_type == 'activity':
                    print(f"  ✨ {item['title']} ({item['duration']}, {item['effort']} effort)")
                    print(f"     {item['description']}")
                elif source_type == 'self_care':
                    print(f"  💆 {item}")
                else:
                    print(f"  📌 {item}")
