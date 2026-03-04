# backend/nlp/sentiment.py
"""
Multi-language sentiment analysis using HuggingFace transformers.
Model: cardiffnlp/twitter-xlm-roberta-base-sentiment
Supports 100+ languages including Hindi, Tamil, Telugu, Bengali etc.
"""
from transformers import pipeline


class SentimentAnalyzer:
    def __init__(self, translator=None):
        print("  Loading sentiment model (first time takes 2-3 min)...")

        self.classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
            top_k=None
        )

        if translator is None:
            from nlp.translator import TranslatorService
            translator = TranslatorService()
        self.translator = translator

        # Label mapping
        self.label_map = {
            "positive": "positive",
            "negative": "negative",
            "neutral": "neutral",
            "LABEL_0": "negative",
            "LABEL_1": "neutral",
            "LABEL_2": "positive"
        }

        print("  Sentiment analyzer ready!")

    def analyze(self, text, translate_first=False, language=None):
        """Analyze sentiment of a single text"""
        if not text or len(text.strip()) < 3:
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "scores": {},
                "language": "unknown"
            }

        # Detect language only if not provided
        if language is None:
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
            print(f"  Sentiment error: {e}")
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "scores": {},
                "language": language
            }

    def analyze_batch(self, texts, batch_size=32, languages=None):
        """Analyze sentiment of multiple texts efficiently"""
        results = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            # Clean batch
            clean_batch = []
            original_texts = []
            batch_indices = []
            for j, t in enumerate(batch):
                if t and len(t.strip()) > 3:
                    clean_batch.append(t[:500])
                    original_texts.append(t)
                    batch_indices.append(i + j)

            if not clean_batch:
                continue

            try:
                batch_results = self.classifier(clean_batch)

                for idx, (text, result) in enumerate(zip(original_texts, batch_results)):
                    if isinstance(result, list):
                        scores = {}
                        for r in result:
                            label = self.label_map.get(r["label"], r["label"])
                            scores[label] = round(r["score"], 4)

                        top = max(scores, key=scores.get)

                        # Use pre-detected language if available
                        if languages and batch_indices[idx] < len(languages):
                            language = languages[batch_indices[idx]]
                        else:
                            language = self.translator.detect_language(text)

                        results.append({
                            "text": text,
                            "sentiment": top,
                            "confidence": scores[top],
                            "scores": scores,
                            "language": language
                        })

            except Exception as e:
                print(f"  Batch error: {e}")
                continue

            processed = min(i + batch_size, len(texts))
            print(f"  Processed {processed}/{len(texts)} texts")

        return results


# Quick test
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()

    test_texts = [
        "Modi ji has done amazing work for India",
        "This government is completely useless and corrupt",
        "The new road construction was inaugurated today",
        "\u092e\u094b\u0926\u0940 \u091c\u0940 \u0928\u0947 \u092c\u0939\u0941\u0924 \u0905\u091a\u094d\u091b\u093e \u0915\u093e\u092e \u0915\u093f\u092f\u093e \u0939\u0948",
        "\u0938\u0930\u0915\u093e\u0930 \u092c\u093f\u0932\u094d\u0915\u0941\u0932 \u092c\u0947\u0915\u093e\u0930 \u0939\u0948",
        "\u0ba8\u0bb2\u0bcd\u0bb2 \u0bb5\u0bc7\u0bb2\u0bc8 \u0b9a\u0bc6\u0baf\u0bcd\u0b95\u0bbf\u0bb1\u0bbe\u0bb0\u0bcd\u0b95\u0bb3\u0bcd",
        "\u09b8\u09b0\u0995\u09be\u09b0 \u09ad\u09be\u09b2\u09cb \u0995\u09be\u099c \u0995\u09b0\u099b\u09c7 \u09a8\u09be",
    ]

    print("\n  Testing sentiment analysis:\n")

    for text in test_texts:
        result = analyzer.analyze(text)
        emoji = {"positive": "+", "negative": "-", "neutral": "~"}
        print(
            f"  {emoji[result['sentiment']]} "
            f"[{result['sentiment'].upper():>8}] "
            f"({result['confidence']:.1%}) "
            f"[{result['language']:>3}] "
            f"-> {text[:60]}"
        )
