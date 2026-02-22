# backend/scrapers/scraper_manager.py
"""
Orchestrates all scrapers — runs them all and combines results.
"""
from datetime import datetime


class ScraperManager:
    def __init__(self):
        print("\n📡 Initializing all scrapers...")

        # Import scrapers
        from scrapers.youtube_scraper import YouTubeScraper
        from scrapers.reddit_scraper import RedditScraper
        from scrapers.news_scraper import NewsScraper
        from scrapers.twitter_scraper import TwitterScraper

        self.youtube = YouTubeScraper()
        self.reddit = RedditScraper()
        self.news = NewsScraper()
        self.twitter = TwitterScraper()

        print("✅ All scrapers ready!\n")

    def scrape_all(self, keywords=None):
        """Run all scrapers and combine results"""
        if keywords is None:
            keywords = [
                "Modi government",
                "India development",
                "BJP Congress",
                "Indian economy",
                "government scheme"
            ]

        all_data = []
        stats = {}

        # 1. YouTube
        print("\n📹 ── YouTube ──")
        try:
            yt_data = self.youtube.scrape_political_comments(
                keywords=keywords[:3], max_videos=2
            )
            all_data.extend(yt_data)
            stats["youtube"] = len(yt_data)
        except Exception as e:
            print(f"  ❌ YouTube failed: {e}")
            stats["youtube"] = 0

        # 2. Reddit
        print("\n📝 ── Reddit ──")
        try:
            reddit_data = self.reddit.scrape_political_data(keywords=keywords)
            all_data.extend(reddit_data)
            stats["reddit"] = len(reddit_data)
        except Exception as e:
            print(f"  ❌ Reddit failed: {e}")
            stats["reddit"] = 0

        # 3. News
        print("\n📰 ── News ──")
        try:
            news_data = self.news.scrape_all_news(keywords=keywords)
            all_data.extend(news_data)
            stats["news"] = len(news_data)
        except Exception as e:
            print(f"  ❌ News failed: {e}")
            stats["news"] = 0

        # 4. Twitter
        print("\n🐦 ── Twitter ──")
        try:
            twitter_data = self.twitter.scrape_political_tweets(keywords=keywords[:3])
            all_data.extend(twitter_data)
            stats["twitter"] = len(twitter_data)
        except Exception as e:
            print(f"  ❌ Twitter failed: {e}")
            stats["twitter"] = 0

        # Summary
        print("\n" + "=" * 50)
        print("📊 SCRAPING SUMMARY")
        print("=" * 50)
        for source, count in stats.items():
            emoji = "✅" if count > 0 else "❌"
            print(f"  {emoji} {source:>10}: {count} items")
        print(f"  {'─' * 30}")
        print(f"  📦 Total: {len(all_data)} items")
        print("=" * 50)

        return all_data, stats

    def scrape_single_source(self, source, keywords=None):
        """Scrape from a single source"""
        if keywords is None:
            keywords = ["Modi government", "India development"]

        if source == "youtube":
            return self.youtube.scrape_political_comments(keywords=keywords, max_videos=2)
        elif source == "reddit":
            return self.reddit.scrape_political_data(keywords=keywords)
        elif source == "news":
            return self.news.scrape_all_news(keywords=keywords)
        elif source == "twitter":
            return self.twitter.scrape_political_tweets(keywords=keywords)
        else:
            print(f"❌ Unknown source: {source}")
            return []


# Quick test
if __name__ == "__main__":
    manager = ScraperManager()
    data, stats = manager.scrape_all(keywords=["Modi government"])
    print(f"\nFirst 3 items:")
    for item in data[:3]:
        print(f"  [{item['source']:>8}] {item['text'][:80]}...")