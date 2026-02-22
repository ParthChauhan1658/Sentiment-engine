# backend/scrapers/twitter_scraper.py
"""
Twitter/X scraper using snscrape.
NOTE: snscrape may not work with latest Twitter/X changes.
This is a best-effort scraper with fallback.
"""
import time


class TwitterScraper:
    def __init__(self):
        self.working = False
        try:
            import snscrape.modules.twitter as sntwitter
            self.sntwitter = sntwitter
            self.working = True
            print("✅ Twitter scraper initialized (snscrape)")
        except ImportError:
            print("⚠️ snscrape not installed. Twitter scraping disabled.")
            print("   Install with: pip install snscrape")
        except Exception as e:
            print(f"⚠️ Twitter scraper init failed: {e}")

    def search_tweets(self, query, limit=100):
        """Search tweets using snscrape"""
        if not self.working:
            print("  ⚠️ Twitter scraper not available, skipping...")
            return []

        tweets = []

        try:
            search_query = f"{query} lang:en OR lang:hi"
            scraper = self.sntwitter.TwitterSearchScraper(search_query)

            for i, tweet in enumerate(scraper.get_items()):
                if i >= limit:
                    break

                tweets.append({
                    "text": tweet.rawContent,
                    "title": "",
                    "author": tweet.user.username if tweet.user else "unknown",
                    "source": "twitter",
                    "url": tweet.url if hasattr(tweet, "url") else "",
                    "location": tweet.user.location if tweet.user and tweet.user.location else "",
                    "language": tweet.lang if hasattr(tweet, "lang") else "unknown",
                    "metadata": {
                        "likes": tweet.likeCount if hasattr(tweet, "likeCount") else 0,
                        "retweets": tweet.retweetCount if hasattr(tweet, "retweetCount") else 0,
                        "date": str(tweet.date) if hasattr(tweet, "date") else ""
                    }
                })

        except Exception as e:
            print(f"  ⚠️ Twitter search failed: {e}")
            print("  (Twitter/X may have blocked snscrape)")

        return tweets

    def scrape_political_tweets(self, keywords=None):
        """Full pipeline: search multiple political keywords"""
        if not self.working:
            return []

        if keywords is None:
            keywords = [
                "Modi India",
                "BJP government",
                "Congress India",
                "India politics",
                "सरकार भारत"
            ]

        all_tweets = []

        for keyword in keywords:
            print(f"  🔍 Twitter search: {keyword}")
            tweets = self.search_tweets(keyword, limit=50)
            all_tweets.extend(tweets)
            print(f"     Found {len(tweets)} tweets")
            time.sleep(2)  # Rate limit protection

        # Remove duplicates
        seen = set()
        unique = []
        for t in all_tweets:
            if t["text"] not in seen:
                seen.add(t["text"])
                unique.append(t)

        print(f"  ✅ Total unique tweets: {len(unique)}")
        return unique


# Quick test
if __name__ == "__main__":
    scraper = TwitterScraper()
    if scraper.working:
        tweets = scraper.scrape_political_tweets(keywords=["Modi India"])
        for t in tweets[:3]:
            print(f"  🐦 {t['text'][:100]}")
            print(f"     ❤️ {t['metadata']['likes']} | 🔄 {t['metadata']['retweets']}")
            print("  ---")
    else:
        print("Twitter scraper not available. Other sources will be used.")