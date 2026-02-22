# backend/scrapers/news_scraper.py
from newsapi import NewsApiClient
import feedparser
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import NEWS_API_KEY


class NewsScraper:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        print("✅ News scraper initialized")

    def get_newsapi_articles(self, query, page_size=50):
        """Get articles from NewsAPI"""
        try:
            response = self.newsapi.get_everything(
                q=query,
                language="en",
                sort_by="publishedAt",
                page_size=min(page_size, 100)
            )

            articles = []
            for item in response.get("articles", []):
                title = item.get("title", "") or ""
                description = item.get("description", "") or ""

                articles.append({
                    "text": f"{title} {description}".strip(),
                    "title": title,
                    "author": item.get("author", "Unknown") or "Unknown",
                    "source": "news",
                    "url": item.get("url", ""),
                    "location": "",
                    "language": "en",
                    "metadata": {
                        "news_source": item.get("source", {}).get("name", "Unknown"),
                        "published": item.get("publishedAt", ""),
                        "image": item.get("urlToImage", "")
                    }
                })

            return articles

        except Exception as e:
            print(f"  ⚠️ NewsAPI failed: {e}")
            return []

    def get_google_news(self, query, language="en"):
        """Get articles from Google News RSS — FREE, no key needed!"""
        lang_map = {
            "en": ("en-IN", "IN"),
            "hi": ("hi-IN", "IN"),
            "ta": ("ta-IN", "IN"),
            "te": ("te-IN", "IN"),
            "bn": ("bn-IN", "IN"),
            "mr": ("mr-IN", "IN"),
        }

        hl, gl = lang_map.get(language, ("en-IN", "IN"))
        encoded_query = query.replace(" ", "+")

        url = (
            f"https://news.google.com/rss/search?"
            f"q={encoded_query}&hl={hl}&gl={gl}&ceid={gl}:{hl.split('-')[0]}"
        )

        try:
            feed = feedparser.parse(url)

            articles = []
            for entry in feed.entries[:50]:
                articles.append({
                    "text": f"{entry.title} {entry.get('summary', '')}".strip(),
                    "title": entry.title,
                    "author": entry.get("source", {}).get("title", "Google News"),
                    "source": "news",
                    "url": entry.link,
                    "location": "",
                    "language": language,
                    "metadata": {
                        "news_source": "Google News",
                        "published": entry.get("published", ""),
                    }
                })

            return articles

        except Exception as e:
            print(f"  ⚠️ Google News ({language}) failed: {e}")
            return []

    def get_top_headlines(self, page_size=20):
        """Get top Indian headlines"""
        try:
            response = self.newsapi.get_top_headlines(
                country="in",
                page_size=page_size
            )

            articles = []
            for item in response.get("articles", []):
                title = item.get("title", "") or ""
                description = item.get("description", "") or ""

                articles.append({
                    "text": f"{title} {description}".strip(),
                    "title": title,
                    "author": item.get("author", "Unknown") or "Unknown",
                    "source": "news",
                    "url": item.get("url", ""),
                    "location": "",
                    "language": "en",
                    "metadata": {
                        "news_source": item.get("source", {}).get("name", "Unknown"),
                        "published": item.get("publishedAt", ""),
                        "type": "headline"
                    }
                })

            return articles

        except Exception as e:
            print(f"  ⚠️ Headlines failed: {e}")
            return []

    def scrape_all_news(self, keywords=None):
        """Full pipeline: collect from all news sources"""
        if keywords is None:
            keywords = [
                "India government policy",
                "Modi BJP development",
                "India infrastructure project",
                "Indian economy growth",
                "India election politics"
            ]

        all_articles = []

        # Top headlines
        print("  🔍 Fetching top headlines...")
        headlines = self.get_top_headlines()
        all_articles.extend(headlines)
        print(f"     Got {len(headlines)} headlines")

        for keyword in keywords:
            # NewsAPI
            print(f"  🔍 NewsAPI: {keyword}")
            articles = self.get_newsapi_articles(keyword, page_size=20)
            all_articles.extend(articles)
            print(f"     Found {len(articles)} articles")

            # Google News English
            print(f"  🔍 Google News (EN): {keyword}")
            articles = self.get_google_news(keyword, "en")
            all_articles.extend(articles)
            print(f"     Found {len(articles)} articles")

            # Google News Hindi
            print(f"  🔍 Google News (HI): {keyword}")
            articles = self.get_google_news(keyword, "hi")
            all_articles.extend(articles)
            print(f"     Found {len(articles)} articles")

        # Remove duplicates by title
        seen = set()
        unique = []
        for a in all_articles:
            if a["title"] and a["title"] not in seen:
                seen.add(a["title"])
                unique.append(a)

        print(f"  ✅ Total unique articles: {len(unique)}")
        return unique


# Quick test
if __name__ == "__main__":
    scraper = NewsScraper()
    articles = scraper.scrape_all_news(keywords=["Modi government"])
    for a in articles[:3]:
        print(f"  📰 {a['title'][:80]}")
        print(f"     Source: {a['metadata'].get('news_source', 'Unknown')}")
        print("  ---")