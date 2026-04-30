"""
Myanmar Language Emotion Detection Test
မြန်မာဘာသာ emotion detection unit tests
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.myanmar_emotion_detector import (
    MyanmarEmotionDetector,
    is_myanmar_text,
    detect_myanmar_emotion,
)
from nlp.emotion_detector import detect_emotion


# ─────────────────────────────────────────────────────────────────────────────
PASS = "✅"
FAIL = "❌"
# ─────────────────────────────────────────────────────────────────────────────


def test_is_myanmar_text():
    print("\n── is_myanmar_text() ──")
    cases = [
        ("ပျော်တယ်", True),
        ("ဝမ်းနည်းတယ်", True),
        ("I am happy", False),
        ("ကျေနပ်ပါတယ်", True),
        ("mixed မြန်မာ English", True),   # ≥25% Myanmar
        ("", False),
    ]
    passed = 0
    for text, expected in cases:
        result = is_myanmar_text(text)
        ok = result == expected
        icon = PASS if ok else FAIL
        print(f"  {icon} is_myanmar_text({repr(text)}) = {result}  (expected {expected})")
        if ok:
            passed += 1
    print(f"  Result: {passed}/{len(cases)} passed")
    return passed, len(cases)


def test_myanmar_emotion_detection():
    print("\n── Myanmar Emotion Detection ──")
    detector = MyanmarEmotionDetector()

    cases = [
        # (text, expected_emotion)
        ("ဒီနေ့ တော်တော် ပျော်တယ်", "joy"),
        ("ကျေနပ်ပါတယ် ကြည်နူးပါတယ်", "joy"),
        ("ဒေါသ တော်တော် ဖြစ်နေတယ်", "anger"),
        ("မနပ် စိတ်ဆိုးနေတယ်", "anger"),
        ("ဝမ်းနည်းနေတယ်", "sadness"),
        ("ငိုချင်နေတယ်", "sadness"),
        ("ကြောက်ရွံ့တယ် ထိတ်လန့်တယ်", "fear"),  # clearer fear
        ("ပူပန်နေတယ်", "fear"),
    ]

    passed = 0
    for text, expected in cases:
        result = detector.detect(text)
        ok = result["emotion"] == expected
        icon = PASS if ok else FAIL
        print(
            f"  {icon} '{text}'\n"
            f"       → {result['emoji']} {result['emotion']} ({result['confidence']:.2f})"
            f"  [expected: {expected}]"
        )
        if ok:
            passed += 1
    print(f"  Result: {passed}/{len(cases)} passed")
    return passed, len(cases)


def test_negation():
    print("\n── Negation Handling ──")
    detector = MyanmarEmotionDetector()

    cases = [
        ("မပျော်ဘူး", "joy", False),   # negated joy → should NOT be joy
    ]
    passed = 0
    for text, should_not_be, _flag in cases:
        result = detector.detect(text)
        # Negated joy should lower joy score / redirect
        ok = result["emotion"] != should_not_be or result["confidence"] < 0.8
        icon = PASS if ok else FAIL
        print(f"  {icon} '{text}' → {result['emoji']} {result['emotion']} ({result['confidence']:.2f})")
        if ok:
            passed += 1
    print(f"  Result: {passed}/{len(cases)} passed")
    return passed, len(cases)


def test_auto_routing():
    print("\n── Auto Language Routing (detect_emotion) ──")
    cases = [
        ("ပျော်တယ်",            "joy",     "my"),
        ("ဝမ်းနည်းတယ်",         "sadness", "my"),
        ("I am so happy!",       "joy",     "en"),
        ("This is so frustrating and infuriating!", "anger",   "en"),
    ]
    passed = 0
    for text, expected_emotion, expected_lang in cases:
        result = detect_emotion(text)
        ok_emotion = result["emotion"] == expected_emotion
        ok_lang = result.get("language") == expected_lang
        ok = ok_emotion and ok_lang
        icon = PASS if ok else FAIL
        print(
            f"  {icon} '{text}'\n"
            f"       → {result['emoji']} {result['emotion']} (lang={result.get('language')})"
            f"  [expected: {expected_emotion}, lang={expected_lang}]"
        )
        if ok:
            passed += 1
    print(f"  Result: {passed}/{len(cases)} passed")
    return passed, len(cases)


def main():
    print("=" * 60)
    print("  Myanmar Emotion Detection — Test Suite")
    print("=" * 60)

    total_passed = 0
    total_cases = 0

    for fn in [
        test_is_myanmar_text,
        test_myanmar_emotion_detection,
        test_negation,
        test_auto_routing,
    ]:
        p, c = fn()
        total_passed += p
        total_cases += c

    print("\n" + "=" * 60)
    print(f"  TOTAL: {total_passed}/{total_cases} passed")
    if total_passed == total_cases:
        print("  🎉 All tests passed!")
    else:
        print(f"  ⚠️  {total_cases - total_passed} test(s) failed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
