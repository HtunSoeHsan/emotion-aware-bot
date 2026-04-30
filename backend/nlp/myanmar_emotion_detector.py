"""
Myanmar Language Emotion Detector
မြန်မာဘာသာ emotion detection using keyword-based approach.
VADER သည် မြန်မာဘာသာကို support မလုပ်သောကြောင့် keyword matching method ကို သုံးသည်။
"""

import re
from typing import Dict, Tuple, List


# ─────────────────────────────────────────────────────────────────────────────
# Myanmar Unicode range: U+1000 – U+109F
# ─────────────────────────────────────────────────────────────────────────────

MYANMAR_UNICODE_RANGE = re.compile(r'[\u1000-\u109F\uAA60-\uAA7F\uA9E0-\uA9FF]')


def is_myanmar_text(text: str) -> bool:
    """
    Myanmar Unicode characters ပါမပါ စစ်ဆေးသည်။
    30% ထက်ပိုသော characters ကို Myanmar ဟု မှတ်ယူသည်။
    """
    if not text:
        return False
    myanmar_chars = len(MYANMAR_UNICODE_RANGE.findall(text))
    total_chars = len([c for c in text if not c.isspace()])
    if total_chars == 0:
        return False
    return (myanmar_chars / total_chars) >= 0.25


# ─────────────────────────────────────────────────────────────────────────────
# Myanmar Emotion Keyword Dictionary
# ─────────────────────────────────────────────────────────────────────────────

MYANMAR_EMOTION_KEYWORDS: Dict[str, List[str]] = {
    'joy': [
        # ပျော်ရွှင်မှု / ဝမ်းသာမှု
        'ပျော်', 'ပျော်ရွှင်', 'ပျော်မြေ့', 'ဝမ်းသာ', 'ကျေနပ်',
        'ကြည်နူး', 'မင်္ဂလာ', 'သာယာ', 'ပီတိ', 'ရွှင်လန်း',
        'ချမ်းမြေ့', 'ထူးခြားသော', 'ကောင်းတယ်', 'ကောင်းလိုက်တာ',
        'အရမ်းကောင်း', 'မျော်မြင်', 'ကံကောင်း', 'ဆုရ', 'အောင်မြင်',
        'မြင်ရ', 'ကြည်နူးရ', 'ဂုဏ်ယူ', 'ချစ်', 'နှစ်သက်',
        'ကြည်ဖြူ', 'ကျေးဇူး', 'ဒိုင်း', 'ကြည်', 'ဒါမှမဟုတ်ဘဲ',
        'ထူးဆန်းသော', 'ကျေးဇူးတင်', 'ကျေးဇူးဩ', 'ဝမ်းမြောက်',
        'ဝမ်းမြောက်ဖွယ်', 'ဂုဏ်ပြု', 'ရွှင်', 'ချမ်း', 'မြေ့',
        'ပျော်ပိုက်', 'ကောင်းမြတ်', 'ဆောင်ရွက်နိုင်', 'ပြည့်ဝ',
        'ဘဝကောင်း', 'မိတ်ဆွေ', 'ချစ်ခင်', 'ကြင်နာ', 'ဦးညွတ်',
        'ကြည်ဖြူ', 'ဒီပဲ', 'ပစ္စုပ္ပန်', 'ထူး', 'ကျေ', 'ဂုဏ်',
        'ကုသိုလ်', 'ဆုတောင်း', 'မင်္ဂလာပါ', 'ဝမ်းမြောက်ပါတယ်',
        'နှစ်သက်ပါတယ်', 'ကျေနပ်ပါတယ်', 'ကောင်းပါတယ်',
    ],
    'anger': [
        # ဒေါသ / မနပ်မနပ်
        'ဒေါသ', 'ဒေါသထွက်', 'ဒေါသဖြစ်', 'မနပ်', 'စိတ်ဆိုး',
        'မကျေနပ်', 'နှောင့်ယှက်', 'ဒုက္ခ', 'ပေါင်းသင်းရ',
        'ဒုက္ခပေး', 'နှောင့်နှေး', 'ရန်', 'ဆဲ', 'ဆဲဆို',
        'ကြောင်', 'ညည်းတွား', 'ငြိုငြင်', 'ဆန့်ကျင်', 'ထိခိုက်',
        'ညစ်ညမ်း', 'ရုန်းကန်', 'ကန့်ကွက်', 'မုန်း', 'မုန်းတီး',
        'ဒေါသကြီး', 'မနှစ်မြို့', 'ဆိုးရွား', 'ရက်စက်',
        'ညစ်', 'ဒေါသဒေါသ', 'ပြောင်ပြောင်', 'မစိတ်ချ',
        'ကျပ်တည်း', 'ကောင်းမွန်ကြောင်း', 'ဆိုးညစ်',
        'ဒေါသမကိုင်', 'ဖျတ်', 'ချုပ်ချယ်',
        'မကြောက်ချင်', 'ဒေါသများ', 'ဒေါသပြ', 'ပြင်းထန်',
        'ဒေါသမနေနိုင်', 'ဒေါသမထိန်းနိုင်', 'ဆဲဆိုသည်',
        'ရန်ဖြစ်', 'ငြိုငြင်မိ', 'ဒေါသဖြစ်မိ',
        'မောင်', 'တင်မြှင့်', 'ကြိတ်', 'ဒေါသကောင်',
    ],
    'sadness': [
        # ဝမ်းနည်းမှု / နာကျင်မှု
        'ဝမ်းနည်း', 'နာကျင်', 'ငိုကြွေး', 'ငို', 'လွမ်းဆွတ်',
        'ပူဆွေး', 'မျက်ရည်', 'ဆုံးရှုံး', 'ကွဲကွာ', 'နောင်တ',
        'နာကျင်', 'ကွဲ', 'ညည်း', 'ညည်းညူ', 'ကပ်',
        'မကောင်း', 'ဒါးနဲ့', 'တမ်းတ', 'ဖွဲ့ဖွဲ့', 'ဖွဲ့',
        'ငိုချင်', 'ငိုမိ', 'ငိုနေ', 'ရင်နင့်', 'ကြေကွဲ',
        'ကြေကွဲမှု', 'ဝမ်းနည်းမှု', 'ကွဲကွာမှု', 'ပူပင်',
        'ကြေမွ', 'ဘဝဆုံးရှုံး', 'မျှော်မှန်းချက်ဆုံး', 'ဆင်းရဲ',
        'ခဲယဉ်း', 'ညင်ညင်', 'ဆင်', 'ဆင်ဆင်', 'ကြိမ်',
        'ဝမ်းနည်းလွန်း', 'နာကျင်လွန်း', 'မနေနိုင်',
        'ငိုလိုက်ချင်', 'ကြေကွဲရ', 'ဒုက္ခရောက်', 'ဒုက္ခတွေ',
    ],
    'fear': [
        # ကြောက်ရွံ့မှု / စိုးရိမ်မှု
        'ကြောက်', 'ကြောက်ရွံ့', 'ကြောက်ရင့်', 'ကြောက်မိ',
        'စိုးရိမ်', 'ပူပန်', 'တုန်လှုပ်', 'ထိတ်လန့်', 'ပူ',
        'ပူပင်', 'ဘေးကြောက်', 'အန္တရာယ်', 'မဆင်ဆင်',
        'မသေချာ', 'မသိ', 'ကြောက်တတ်', 'ထောင်',
        'ခြောက်', 'ငတ်', 'ကြောက်မျိုး', 'ကြောက်မှတ်',
        'ကြောက်နေ', 'ပူပင်နေ', 'စိုးရိမ်နေ', 'တုန်',
        'ရင်တုန်', 'နှလုံးတုန်', 'ကြောက်ချင်', 'ပြေး',
        'ရှောင်', 'ဖြစ်မည်ကြောက်', 'ဘာဖြစ်မလဲ', 'ဘာဖြစ်မှာလဲ',
        'နောင်ကြောင့်', 'ပူဆဲ', 'တုန်လှုပ်နေ',
        'ကြောက်ရွံ့နေ', 'ကြောက်မိ', 'ထိတ်',
        'ထိတ်ထိတ်', 'ကြောက်ကြောက်',
        # compound forms
        'ကြောက်နေမိ', 'ကြောက်လာ', 'ကြောက်ကြောင်',
        'ထိတ်လန့်နေ', 'စိုးရိမ်မိ', 'ပူပန်မိ',
    ],
}

# Negation patterns (မ...ဘူး / မ...တာ)
NEGATION_PATTERNS = [
    re.compile(r'မ(\S+?)ဘူး'),
    re.compile(r'မ(\S+?)တော့'),
    re.compile(r'မ(\S+?)နဲ့'),
    re.compile(r'မ(\S+?)လိုက်ပါ'),
    re.compile(r'မ(\S+?)'),  # ← general မ prefix
]

# Booster words (emotion intensity ကို မြင့်တင်သည်)
BOOSTER_WORDS = [
    'အရမ်း', 'တော်တော်', 'ဆိုးဆိုး', 'ကြီးကြီး', 'များများ',
    'ထပ်ပိုပြီး', 'ပြင်းပြင်း', 'လွန်', 'မကြာမြင့်မီ', 'ကြောက်ကြောက်',
    'အများကြီး', 'ကြာကြာ', 'တစ်ချက်', 'တော်တော်လေး', 'ကလေး',
]

# Emotion UI metadata
EMOTION_EMOJIS = {
    'joy': '😊',
    'anger': '😠',
    'sadness': '😢',
    'fear': '😨',
    'neutral': '😐',
}

EMOTION_COLORS = {
    'joy': 'green',
    'anger': 'red',
    'sadness': 'blue',
    'fear': 'purple',
    'neutral': 'gray',
}


# ─────────────────────────────────────────────────────────────────────────────
# Myanmar Emotion Detector
# ─────────────────────────────────────────────────────────────────────────────

class MyanmarEmotionDetector:
    """
    မြန်မာဘာသာ keyword-based emotion detector.

    Algorithm:
      1. text ကို tokenize (space + Burmese syllable boundary)
      2. Negation context စစ်ဆေး
      3. ကျင့်ဝတ်မှာပါတဲ့ keyword တွေကို count
      4. Booster word ရှိရင် confidence ကို မြင့်တင်
      5. Most frequent emotion ကို return
    """

    def __init__(self):
        self.keywords = MYANMAR_EMOTION_KEYWORDS

    def _tokenize(self, text: str) -> List[str]:
        """Basic Myanmar tokenizer (whitespace + punctuation split)"""
        # Remove punctuation variants
        text = re.sub(r'[၊။!?.,]', ' ', text)
        return text.split()

    def _check_negation(self, token: str) -> bool:
        """မ prefix ပါမပါ စစ်ဆေး"""
        return token.startswith('မ')

    def _count_booster(self, tokens: List[str]) -> float:
        """Booster words ရှိမရှိ စစ်ဆေးပြီး multiplier return"""
        for token in tokens:
            for booster in BOOSTER_WORDS:
                if booster in token:
                    return 1.3  # 30% confidence boost
        return 1.0

    def detect(self, text: str) -> Dict:
        """
        မြန်မာ text မှ emotion ရှာဖွေသည်။

        Args:
            text: မြန်မာ input text

        Returns:
            emotion, confidence, emoji, color, scores ပါဝင်သော dict
        """
        tokens = self._tokenize(text)
        booster_multiplier = self._count_booster(tokens)

        # Emotion scores — 'neutral' ပါ ထည့်ထားရမည်
        ALL_EMOTIONS = list(MYANMAR_EMOTION_KEYWORDS.keys()) + ['neutral']
        scores: Dict[str, float] = {e: 0.0 for e in ALL_EMOTIONS}

        # Build a flat set of all known emotion keywords for negation bypass
        ALL_KNOWN_KEYWORDS: set = set()
        for kw_list in self.keywords.values():
            ALL_KNOWN_KEYWORDS.update(kw_list)

        negation_window = False  # မ prefix ရှိပါက နောက် token ကို flip

        for i, token in enumerate(tokens):
            # Negation check — skip if token IS itself a known emotion keyword
            # (e.g. 'မနပ်' is an anger keyword, not a negation)
            if self._check_negation(token) and token not in ALL_KNOWN_KEYWORDS and len(token) >= 3:
                negation_window = True

            for emotion, kw_list in self.keywords.items():
                for kw in kw_list:
                    if kw in token or token in kw:
                        if negation_window and emotion in ('joy', 'sadness') and token not in ALL_KNOWN_KEYWORDS:
                            # Negated emotion → add to neutral instead
                            scores['neutral'] += 0.5
                        else:
                            scores[emotion] += 1.0
                        break  # တစ် keyword တွေ့ပြီဆိုရင် ထွက်

            # Reset negation window after 2 tokens
            if negation_window and i > 0:
                negation_window = False

        total = sum(scores.values())

        if total == 0:
            # Keyword မတွေ့ → neutral
            return {
                'emotion': 'neutral',
                'confidence': 0.5,
                'emoji': EMOTION_EMOJIS['neutral'],
                'color': EMOTION_COLORS['neutral'],
                'scores': {e: 0.0 for e in scores},
                'language': 'my',
                'method': 'myanmar_keyword',
            }

        # Normalize scores
        normalized: Dict[str, float] = {e: round(s / total, 3) for e, s in scores.items()}

        # Best emotion
        best_emotion = max(normalized, key=lambda e: normalized[e])
        raw_confidence = normalized[best_emotion] * booster_multiplier
        confidence = min(1.0, raw_confidence)

        return {
            'emotion': best_emotion,
            'confidence': round(confidence, 3),
            'emoji': EMOTION_EMOJIS[best_emotion],
            'color': EMOTION_COLORS[best_emotion],
            'scores': normalized,
            'language': 'my',
            'method': 'myanmar_keyword',
        }


# ─────────────────────────────────────────────────────────────────────────────
# Singleton + Convenience
# ─────────────────────────────────────────────────────────────────────────────

_detector = None


def get_myanmar_detector() -> MyanmarEmotionDetector:
    global _detector
    if _detector is None:
        _detector = MyanmarEmotionDetector()
    return _detector


def detect_myanmar_emotion(text: str) -> Dict:
    """
    မြန်မာ text မှ emotion detect လုပ်ရန် convenience function

    Args:
        text: မြန်မာ input text

    Returns:
        Emotion detection result dict
    """
    return get_myanmar_detector().detect(text)


# ─────────────────────────────────────────────────────────────────────────────
# Standalone test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    detector = MyanmarEmotionDetector()

    test_cases = [
        "ဒီနေ့ တော်တော် ပျော်တယ်",
        "ဒေါသ တော်တော် ဖြစ်နေတယ်",
        "ဝမ်းနည်းနေတယ်",
        "ကြောက်နေမိတယ်",
        "မပျော်ဘူး",                  # negation test
        "ကျေနပ်ပါတယ် ကျေးဇူးတင်ပါတယ်",
    ]

    print("Myanmar Emotion Detector Test")
    print("=" * 50)
    for text in test_cases:
        result = detector.detect(text)
        print(f"\nText  : {text}")
        print(f"Emotion: {result['emoji']} {result['emotion']} ({result['confidence']:.3f})")
        print(f"Scores : {result['scores']}")
