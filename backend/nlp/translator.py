# backend/nlp/translator.py
from deep_translator import GoogleTranslator
import re


class TranslatorService:
    def __init__(self):
        self.translator = GoogleTranslator(source="auto", target="en")
        self._translators = {"en": self.translator}

        # Common Hinglish words to detect Roman Hindi
        self.hinglish_words = {
            "hai", "hain", "nahi", "nahin", "kya", "kaise", "kab",
            "kon", "kaun", "kaha", "kahaan", "kyun", "kyon",
            "acha", "accha", "bahut", "bohot", "bhi", "aur",
            "lekin", "magar", "par", "agar", "toh", "phir",
            "yeh", "woh", "ye", "wo", "iska", "uska",
            "sabse", "sab", "kuch", "koi", "kitna",
            "desh", "sarkar", "sarkaar", "pradhan", "mantri",
            "chunav", "chunaav", "janta", "janata", "neta",
            "modi", "bjp", "congress", "aap",
            "ji", "sahab", "sahib", "bhai", "didi",
            "paisa", "paise", "rupay", "crore", "lakh",
            "ghar", "sadak", "bijli", "paani", "pani",
            "kaam", "karna", "karke", "karenge", "karega",
            "hoga", "hogi", "honge", "tha", "thi", "the",
            "chahiye", "chahte", "sakta", "sakti", "sakte",
            "jitna", "jeetna", "haarna", "milega", "milegi",
            "rajya", "dilli", "gaon", "sheher",
            "janta", "log", "logo", "logon",
            "bahut", "zyada", "kam", "thoda",
            "achha", "bura", "sahi", "galat",
            "liye", "wale", "wala", "wali",
            "mai", "mein", "se", "ko", "ka", "ki", "ke",
            "pe", "tak", "ab", "jab", "tab",
        }

        print("  Translator initialized (deep-translator + Hinglish detection)")

    def translate_to_english(self, text):
        if not text or len(text.strip()) < 2:
            return text
        try:
            text = text[:4500]
            translated = self.translator.translate(text)
            return translated if translated else text
        except Exception:
            return text

    def translate(self, text, target="en"):
        if not text or len(text.strip()) < 2:
            return text
        try:
            if target not in self._translators:
                self._translators[target] = GoogleTranslator(source="auto", target=target)
            translated = self._translators[target].translate(text[:4500])
            return translated if translated else text
        except Exception:
            return text

    def detect_language(self, text):
        """Improved language detection with Hinglish support"""
        if not text:
            return "unknown"

        # Check for Indian scripts first
        for char in text:
            if "\u0900" <= char <= "\u097F":
                return "hi"  # Devanagari (Hindi/Marathi)
            if "\u0B80" <= char <= "\u0BFF":
                return "ta"  # Tamil
            if "\u0C00" <= char <= "\u0C7F":
                return "te"  # Telugu
            if "\u0980" <= char <= "\u09FF":
                return "bn"  # Bengali
            if "\u0A80" <= char <= "\u0AFF":
                return "gu"  # Gujarati
            if "\u0C80" <= char <= "\u0CFF":
                return "kn"  # Kannada
            if "\u0D00" <= char <= "\u0D7F":
                return "ml"  # Malayalam
            if "\u0A00" <= char <= "\u0A7F":
                return "pa"  # Punjabi
            if "\u0600" <= char <= "\u06FF":
                return "ur"  # Urdu

        # Check for Hinglish (Hindi written in Roman script)
        words = set(re.findall(r'[a-zA-Z]+', text.lower()))
        if words:
            hinglish_count = len(words.intersection(self.hinglish_words))
            hinglish_ratio = hinglish_count / len(words)

            if hinglish_ratio > 0.2 and hinglish_count >= 2:
                return "hi-Latn"  # Hinglish (Romanized Hindi)

        # Default to English
        ascii_count = sum(1 for c in text if c.isascii())
        if ascii_count / max(len(text), 1) > 0.8:
            return "en"

        return "unknown"

    def detect_and_translate(self, text):
        language = self.detect_language(text)
        if language == "en":
            return text, language
        translated = self.translate_to_english(text)
        return translated, language


if __name__ == "__main__":
    t = TranslatorService()

    tests = [
        "Modi ji has done great work",
        "\u092e\u094b\u0926\u0940 \u091c\u0940 \u0928\u0947 \u092c\u0939\u0941\u0924 \u0905\u091a\u094d\u091b\u093e \u0915\u093e\u092e \u0915\u093f\u092f\u093e",
        "Ye har rajya mai chunaav jitna chahte hai",
        "Sarkar bahut buri hai desh ka kuch nahi ho raha",
        "\u0ba8\u0bb2\u0bcd\u0bb2 \u0bb5\u0bc7\u0bb2\u0bc8 \u0b9a\u0bc6\u0baf\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0bb0\u0bcd\u0b95\u0bb3\u0bcd",
        "Government is corrupt and useless",
        "Tum logo ko des mai jaghe nahi milegi",
    ]

    print("\n  Language Detection Tests:\n")
    for text in tests:
        lang = t.detect_language(text)
        print(f"  [{lang:>7}] {text[:60]}")
