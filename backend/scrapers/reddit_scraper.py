# backend/scrapers/reddit_scraper.py
import requests
import time


class RedditScraper:
    """Uses Arctic Shift API — No API key needed!"""

    def __init__(self):
        self.arctic_url = "https://arctic-shift.photon-reddit.com/api"
        self.pullpush_url = "https://api.pullpush.io"
        self.reddit_json_url = "https://old.reddit.com"
        print("✅ Reddit scraper initialized (Arctic Shift)")

    def search_posts(self, query, subreddits=None, limit=100):
        """Search Reddit posts via Arctic Shift"""
        if subreddits is None:
            subreddits = "india,IndiaSpeaks,indianpolitics"

        if isinstance(subreddits, list):
            subreddits = ",".join(subreddits)

        # Try Arctic Shift first
        posts = self._arctic_shift_search(query, subreddits, limit)

        # Fallback to PullPush
        if not posts:
            posts = self._pullpush_search(query, subreddits, limit)

        # Fallback to Reddit JSON
        if not posts:
            posts = self._reddit_json_search(query, subreddits.split(",")[0], limit)

        return posts

    def _arctic_shift_search(self, query, subreddits, limit):
        """Primary: Arctic Shift API"""
        try:
            url = f"{self.arctic_url}/posts/search"
            params = {
                "subreddit": subreddits,
                "query": query,
                "limit": min(limit, 100),
                "sort": "created_utc",
                "order": "desc"
            }

            response = requests.get(url, params=params, timeout=15)
            data = response.json()

            posts = []
            for post in data.get("data", []):
                posts.append({
                    "text": f"{post.get('title', '')} {post.get('selftext', '')}".strip(),
                    "title": post.get("title", ""),
                    "author": post.get("author", ""),
                    "source": "reddit",
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "location": "",
                    "language": "unknown",
                    "metadata": {
                        "subreddit": post.get("subreddit", ""),
                        "score": post.get("score", 0),
                        "num_comments": post.get("num_comments", 0),
                        "created_utc": post.get("created_utc", 0)
                    }
                })

            return posts

        except Exception as e:
            print(f"  ⚠️ Arctic Shift failed: {e}")
            return []

    def _pullpush_search(self, query, subreddits, limit):
        """Fallback 1: PullPush API"""
        print("  🔄 Trying PullPush fallback...")
        try:
            url = f"{self.pullpush_url}/reddit/search/submission/"
            params = {
                "subreddit": subreddits,
                "q": query,
                "size": min(limit, 100)
            }

            response = requests.get(url, params=params, timeout=15)
            data = response.json()

            posts = []
            for post in data.get("data", []):
                posts.append({
                    "text": f"{post.get('title', '')} {post.get('selftext', '')}".strip(),
                    "title": post.get("title", ""),
                    "author": post.get("author", ""),
                    "source": "reddit",
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "location": "",
                    "language": "unknown",
                    "metadata": {
                        "subreddit": post.get("subreddit", ""),
                        "score": post.get("score", 0),
                        "num_comments": post.get("num_comments", 0)
                    }
                })

            return posts

        except Exception as e:
            print(f"  ⚠️ PullPush failed: {e}")
            return []

    def _reddit_json_search(self, query, subreddit, limit):
        """Fallback 2: Reddit's own JSON endpoint"""
        print("  🔄 Trying Reddit JSON fallback...")
        try:
            url = f"{self.reddit_json_url}/r/{subreddit}/search.json"
            params = {
                "q": query,
                "sort": "new",
                "limit": min(limit, 25),
                "restrict_sr": "on"
            }
            headers = {"User-Agent": "sentiment-engine-hackathon/1.0"}

            response = requests.get(url, params=params, headers=headers, timeout=15)
            data = response.json()

            posts = []
            for child in data.get("data", {}).get("children", []):
                post = child["data"]
                posts.append({
                    "text": f"{post.get('title', '')} {post.get('selftext', '')}".strip(),
                    "title": post.get("title", ""),
                    "author": post.get("author", ""),
                    "source": "reddit",
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "location": "",
                    "language": "unknown",
                    "metadata": {
                        "subreddit": post.get("subreddit", ""),
                        "score": post.get("score", 0),
                        "num_comments": post.get("num_comments", 0)
                    }
                })

            return posts

        except Exception as e:
            print(f"  ❌ Reddit JSON also failed: {e}")
            return []

    def scrape_political_data(self, keywords=None):
        """Full pipeline: search multiple political keywords"""
        if keywords is None:
            keywords = [
                "Modi government",
                "BJP Congress",
                "India development",
                "water crisis India",
                "Indian economy",
                "government scheme India"
            ]

        all_posts = []

        for keyword in keywords:
            print(f"  🔍 Reddit search: {keyword}")
            posts = self.search_posts(keyword, limit=50)
            all_posts.extend(posts)
            print(f"     Found {len(posts)} posts")
            time.sleep(1)  # Be respectful

        # Remove duplicates by URL
        seen = set()
        unique_posts = []
        for post in all_posts:
            if post["url"] not in seen:
                seen.add(post["url"])
                unique_posts.append(post)

        print(f"  ✅ Total unique Reddit posts: {len(unique_posts)}")
        return unique_posts


# Quick test
if __name__ == "__main__":
    scraper = RedditScraper()
    posts = scraper.scrape_political_data(keywords=["Modi government"])
    for p in posts[:3]:
        print(f"  📝 {p['title'][:80]}")
        print(f"     r/{p['metadata']['subreddit']} | Score: {p['metadata']['score']}")
        print("  ---")