# backend/services.py
"""
Shared singleton service registry — initialized once at startup.
All heavy NLP models and services are loaded here and shared across all requests.
"""


class Services:
    analyzer = None
    topic_extractor = None
    translator = None
    mapper = None
    booth_mapper = None
    summarizer = None
    scraper_manager = None

    @classmethod
    def initialize(cls):
        from nlp.translator import TranslatorService
        from nlp.sentiment import SentimentAnalyzer
        from nlp.topics import TopicExtractor
        from geo.constituency_mapper import ConstituencyMapper
        from geo.booth_mapper import BoothMapper
        from nlp.summarizer import Summarizer
        from scrapers.scraper_manager import ScraperManager

        print("  [1/7] Translator...")
        cls.translator = TranslatorService()

        print("  [2/7] Sentiment model...")
        cls.analyzer = SentimentAnalyzer(translator=cls.translator)

        print("  [3/7] Topic extractor...")
        cls.topic_extractor = TopicExtractor(translator=cls.translator)

        print("  [4/7] Constituency mapper...")
        cls.mapper = ConstituencyMapper()

        print("  [5/7] Booth mapper...")
        cls.booth_mapper = BoothMapper()

        print("  [6/7] Summarizer...")
        cls.summarizer = Summarizer()

        print("  [7/7] Scraper manager...")
        cls.scraper_manager = ScraperManager()

    @classmethod
    def is_ready(cls):
        return cls.analyzer is not None
