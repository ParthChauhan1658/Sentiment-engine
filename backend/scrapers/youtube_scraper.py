# backend/scrapers/youtube_scraper.py
from googleapiclient.discovery import build
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY


class YouTubeScraper:
    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        print("✅ YouTube scraper initialized")

    def search_videos(self, query, max_results=10):
        """Search for political videos"""
        try:
            request = self.youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=max_results,
                relevanceLanguage="hi",
                regionCode="IN",
                order="date"
            )
            response = request.execute()

            videos = []
            for item in response.get("items", []):
                videos.append({
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel": item["snippet"]["channelTitle"],
                    "published": item["snippet"]["publishedAt"]
                })

            return videos

        except Exception as e:
            print(f"⚠️ YouTube search failed: {e}")
            return []

    def get_comments(self, video_id, max_results=100):
        """Extract comments from a video"""
        comments = []

        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_results, 100),
                textFormat="plainText",
                order="relevance"
            )
            response = request.execute()

            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "text": comment["textDisplay"],
                    "title": "",
                    "author": comment["authorDisplayName"],
                    "source": "youtube",
                    "url": f"https://youtube.com/watch?v={video_id}",
                    "location": "",
                    "language": "unknown",
                    "metadata": {
                        "video_id": video_id,
                        "like_count": comment["likeCount"],
                        "published": comment["publishedAt"]
                    }
                })

        except Exception as e:
            print(f"⚠️ Could not get comments for {video_id}: {e}")

        return comments

    def scrape_political_comments(self, keywords=None, max_videos=3):
        """Full pipeline: search videos → extract comments"""
        if keywords is None:
            keywords = [
                "Modi government 2025",
                "BJP Congress debate",
                "India development news",
                "सरकार योजना",
                "Indian politics today"
            ]

        all_comments = []

        for keyword in keywords:
            print(f"  🔍 YouTube search: {keyword}")
            videos = self.search_videos(keyword, max_results=max_videos)

            for video in videos:
                print(f"    📹 Comments: {video['title'][:50]}...")
                comments = self.get_comments(video["video_id"])
                all_comments.extend(comments)
                print(f"       Got {len(comments)} comments")

        print(f"  ✅ Total YouTube comments: {len(all_comments)}")
        return all_comments


# Quick test
if __name__ == "__main__":
    scraper = YouTubeScraper()
    comments = scraper.scrape_political_comments(
        keywords=["Modi government"],
        max_videos=2
    )
    for c in comments[:3]:
        print(f"  💬 {c['text'][:100]}")
        print(f"     👍 {c['metadata']['like_count']} likes")
        print("  ---")