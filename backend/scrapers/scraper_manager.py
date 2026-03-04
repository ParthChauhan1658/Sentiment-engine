# backend/scrapers/scraper_manager.py
"""
Orchestrates all scrapers — runs them in parallel and combines results.
"""
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class ScraperManager:
    def __init__(self):
        print("\n  Initializing all scrapers...")

        from scrapers.youtube_scraper import YouTubeScraper
        from scrapers.reddit_scraper import RedditScraper
        from scrapers.news_scraper import NewsScraper
        from scrapers.twitter_scraper import TwitterScraper

        self.youtube = YouTubeScraper()
        self.reddit = RedditScraper()
        self.news = NewsScraper()
        self.twitter = TwitterScraper()

        print("  All scrapers ready!\n")

    def scrape_all(self, keywords=None):
        """Run all scrapers in parallel and combine results"""
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

        def _scrape_youtube():
            return "youtube", self.youtube.scrape_political_comments(
                keywords=keywords[:3], max_videos=2
            )

        def _scrape_reddit():
            return "reddit", self.reddit.scrape_political_data(keywords=keywords)

        def _scrape_news():
            return "news", self.news.scrape_all_news(keywords=keywords)

        def _scrape_twitter():
            return "twitter", self.twitter.scrape_political_tweets(keywords=keywords[:3])

        scrapers = [_scrape_youtube, _scrape_reddit, _scrape_news, _scrape_twitter]

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(fn): fn.__name__ for fn in scrapers}

            for future in as_completed(futures):
                name = futures[future]
                try:
                    source, data = future.result(timeout=120)
                    all_data.extend(data)
                    stats[source] = len(data)
                    print(f"  + {source}: {len(data)} items")
                except Exception as e:
                    print(f"  - {name} failed: {e}")

        # Summary
        print("\n" + "=" * 50)
        print("  SCRAPING SUMMARY")
        print("=" * 50)
        for source, count in stats.items():
            emoji = "+" if count > 0 else "-"
            print(f"  {emoji} {source:>10}: {count} items")
        print(f"  Total: {len(all_data)} items")
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
            print(f"  Unknown source: {source}")
            return []


# Quick test
if __name__ == "__main__":
    manager = ScraperManager()
    data, stats = manager.scrape_all(keywords=["Modi government"])
    print(f"\nFirst 3 items:")
    for item in data[:3]:
        print(f"  [{item['source']:>8}] {item['text'][:80]}...")
