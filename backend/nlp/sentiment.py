# backend/nlp/sentiment.py
"""
Multi-language sentiment analysis using HuggingFace transformers.
Model: cardiffnlp/twitter-xlm-roberta-base-sentiment
Supports 100+ languages including Hindi, Tamil, Telugu, Bengali etc.
"""
from transformers import pipeline
from nlp.translator import TranslatorService


class SentimentAnalyzer:
    def __init__(self):
        print("🧠 Loading sentiment model (first time takes 2-3 min)...")

        self.classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
            top_k=None
        )

        self.translator = TranslatorService()

        # Label mapping
        self.label_map = {
            "positive": "positive",
            "negative": "negative",
            "neutral": "neutral",
            "LABEL_0": "negative",
            "LABEL_1": "neutral",
            "LABEL_2": "positive"
        }

        print("✅ Sentiment analyzer ready!")

    def analyze(self, text, translate_first=False):
        """Analyze sentiment of a single text"""
        if not text or len(text.strip()) < 3:
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "scores": {},
                "language": "unknown"
            }

        # Detect language
        language = self.translator.detect_language(text)

        # Truncate for model
        analysis_text = text[:500]

        # Optionally translate first
        if translate_first and language != "en":
            analysis_text = self.translator.translate_to_english(analysis_text)

        try:
            results = self.classifier(analysis_text)

            if isinstance(results[0], list):
                results = results[0]

            scores = {}
            for r in results:
                label = self.label_map.get(r["label"], r["label"])
                scores[label] = round(r["score"], 4)

            top = max(scores, key=scores.get)

            return {
                "sentiment": top,
                "confidence": scores[top],
                "scores": scores,
                "language": language
            }

        except Exception as e:
            print(f"  ⚠️ Sentiment error: {e}")
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "scores": {},
                "language": language
            }

    def analyze_batch(self, texts, batch_size=32):
        """Analyze sentiment of multiple texts efficiently"""
        results = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            # Clean batch
            clean_batch = []
            original_texts = []
            for t in batch:
                if t and len(t.strip()) > 3:
                    clean_batch.append(t[:500])
                    original_texts.append(t)

            if not clean_batch:
                continue

            try:
                batch_results = self.classifier(clean_batch)

                for text, result in zip(original_texts, batch_results):
                    if isinstance(result, list):
                        scores = {}
                        for r in result:
                            label = self.label_map.get(r["label"], r["label"])
                            scores[label] = round(r["score"], 4)

                        top = max(scores, key=scores.get)
                        language = self.translator.detect_language(text)

                        results.append({
                            "text": text,
                            "sentiment": top,
                            "confidence": scores[top],
                            "scores": scores,
                            "language": language
                        })

            except Exception as e:
                print(f"  ⚠️ Batch error: {e}")
                continue

            processed = min(i + batch_size, len(texts))
            print(f"  📊 Processed {processed}/{len(texts)} texts")

        return results


# Quick test
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()

    test_texts = [
        "Modi ji has done amazing work for India",
        "This government is completely useless and corrupt",
        "The new road construction was inaugurated today",
        "मोदी जी ने बहुत अच्छा काम किया है",
        "सरकार बिल्कुल बेकार है",
        "நல்ல வேலை செய்கிறார்கள்",
        "সরকার ভালো কাজ করছে না",
    ]

    print("\n🧪 Testing sentiment analysis:\n")

    for text in test_texts:
        result = analyzer.analyze(text)
        emoji = {"positive": "😊", "negative": "😡", "neutral": "😐"}
        print(
            f"  {emoji[result['sentiment']]} "
            f"[{result['sentiment'].upper():>8}] "
            f"({result['confidence']:.1%}) "
            f"[{result['language']:>3}] "
            f"→ {text[:60]}"
        )