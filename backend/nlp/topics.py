# backend/nlp/topics.py
from nlp.translator import TranslatorService


class TopicExtractor:
    def __init__(self):
        self.translator = TranslatorService()

        try:
            from keybert import KeyBERT
            self.model = KeyBERT()
            self.working = True
            print("✅ Topic extractor initialized (KeyBERT)")
        except Exception as e:
            print(f"⚠️ KeyBERT not available: {e}")
            self.working = False

        # Predefined political topics to look for
        self.political_keywords = [
            "water", "water supply", "road", "roads", "electricity", "power",
            "education", "school", "college", "healthcare", "hospital",
            "employment", "jobs", "unemployment", "inflation", "price rise",
            "corruption", "scam", "development", "infrastructure",
            "farmer", "agriculture", "youth", "women", "safety",
            "subsidy", "scheme", "tax", "gst", "economy", "gdp",
            "security", "defence", "defense", "army", "military",
            "pollution", "environment", "climate", "flood", "drought",
            "housing", "transport", "metro", "railway", "highway",
            "digital", "internet", "technology", "startup",
            "poverty", "hunger", "ration", "gas", "petrol", "diesel",
            "modi", "bjp", "congress", "aap", "opposition",
            "election", "vote", "democracy", "parliament",
            "caste", "reservation", "religion", "communal",
            "media", "press", "freedom", "rights",
        ]

    def extract_topics(self, text, top_n=5):
        """Extract topics — translate non-English first"""
        if not text or len(text.strip()) < 10:
            return []

        # Detect language and translate if needed
        language = self.translator.detect_language(text)
        analysis_text = text

        if language != "en":
            try:
                translated = self.translator.translate_to_english(text)
                if translated and len(translated) > 5:
                    analysis_text = translated
            except:
                pass

        # Method 1: Try KeyBERT
        if self.working:
            try:
                keywords = self.model.extract_keywords(
                    analysis_text,
                    keyphrase_ngram_range=(1, 2),
                    stop_words="english",
                    top_n=top_n,
                    use_mmr=True,
                    diversity=0.5
                )
                topics = [kw[0].lower() for kw in keywords if len(kw[0]) > 2]
                if topics:
                    return topics
            except:
                pass

        # Method 2: Keyword matching fallback
        return self._keyword_match(analysis_text, top_n)

    def _keyword_match(self, text, top_n=5):
        """Fallback: match against predefined political keywords"""
        text_lower = text.lower()
        found = []

        for keyword in self.political_keywords:
            if keyword in text_lower:
                found.append(keyword)

        return found[:top_n] if found else []

    def extract_topics_batch(self, texts, top_n=5):
        all_topics = []
        for text in texts:
            topics = self.extract_topics(text, top_n)
            all_topics.append(topics)
        return all_topics

    def get_common_topics(self, texts, top_n=20):
        topic_counts = {}
        for text in texts:
            topics = self.extract_topics(text, top_n=3)
            for topic in topics:
                topic_lower = topic.lower()
                topic_counts[topic_lower] = topic_counts.get(topic_lower, 0) + 1

        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"name": t[0], "count": t[1]} for t in sorted_topics[:top_n]]


if __name__ == "__main__":
    extractor = TopicExtractor()

    tests = [
        "The government should focus on water supply and road infrastructure",
        "Inflation is rising and employment is declining",
        "मोदी जी ने नई शिक्षा नीति की घोषणा की",
        "Ye sarkar kuch nahi kar rahi paani ki samasya bahut badi hai",
        "Corruption is destroying our democracy",
    ]

    print("\n🏷️ Topic Extraction Tests:\n")
    for text in tests:
        topics = extractor.extract_topics(text)
        print(f"  📝 \"{text[:60]}...\"")
        print(f"  🏷️  Topics: {topics}")
        print()