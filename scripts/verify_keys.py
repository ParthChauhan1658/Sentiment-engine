# scripts/verify_keys.py
"""
Verify all API keys are working.
Run from project root: python scripts/verify_keys.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("=" * 55)
print("  🔍 SENTIMENT ENGINE — API KEY VERIFICATION")
print("=" * 55)
print()

passed = 0
failed = 0

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")


# 1. YouTube
try:
    from googleapiclient.discovery import build
    youtube = build("youtube", "v3",
                    developerKey=os.getenv("YOUTUBE_API_KEY"))
    youtube.search().list(q="India", part="snippet",
                          maxResults=1).execute()
    print("✅ [1/8] YouTube API — WORKING")
    passed += 1
except Exception as e:
    print(f"❌ [1/8] YouTube API — FAILED: {e}")
    failed += 1

# 2. Reddit (Arctic Shift)
try:
    import requests
    url = "https://arctic-shift.photon-reddit.com/api/posts/search"
    params = {"subreddit": "india", "query": "test", "limit": 3}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    count = len(data.get("data", []))
    print(f"✅ [2/8] Reddit (Arctic Shift) — WORKING | Got {count} posts")
    passed += 1
except Exception as e:
    print(f"❌ [2/8] Reddit — FAILED: {e}")
    failed += 1

# 3. NewsAPI
try:
    from newsapi import NewsApiClient
    newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
    result = newsapi.get_top_headlines(country="in", page_size=1)
    print("✅ [3/8] NewsAPI — WORKING")
    passed += 1
except Exception as e:
    print(f"❌ [3/8] NewsAPI — FAILED: {e}")
    failed += 1

# 4. Google News RSS (no key)
try:
    import feedparser
    feed = feedparser.parse(
        "https://news.google.com/rss/search?q=india&hl=en-IN&gl=IN"
    )
    if len(feed.entries) > 0:
        print(f"✅ [4/8] Google News RSS — WORKING | Got {len(feed.entries)} articles")
    else:
        print("⚠️  [4/8] Google News RSS — Connected but no data")
    passed += 1
except Exception as e:
    print(f"❌ [4/8] Google News RSS — FAILED: {e}")
    failed += 1

# 5. Gemini (NEW google-genai package)
try:
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello in one word"
    )
    print(f"✅ [5/8] Gemini API — WORKING | Response: {response.text[:30]}")
    passed += 1
except Exception as e:
    print(f"❌ [5/8] Gemini API — FAILED: {e}")
    failed += 1

# 6. Groq
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say hi in 3 words"}],
        max_tokens=10
    )
    reply = response.choices[0].message.content
    print(f"✅ [6/8] Groq API — WORKING | Response: {reply}")
    passed += 1
except Exception as e:
    print(f"❌ [6/8] Groq API — FAILED: {e}")
    failed += 1

# 7. MongoDB (with SSL fix)
try:
    from pymongo import MongoClient
    import certifi

    client = MongoClient(
        os.getenv("MONGODB_URI"),
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )
    client.admin.command("ping")
    print("✅ [7/8] MongoDB Atlas — WORKING")
    passed += 1
except Exception as e:
    print(f"❌ [7/8] MongoDB Atlas — FAILED: {e}")
    failed += 1

# 8. Telegram
try:
    import requests as req
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    r = req.get(f"https://api.telegram.org/bot{token}/getMe")
    bot_name = r.json()["result"]["username"]
    print(f"✅ [8/8] Telegram Bot — WORKING | Bot: @{bot_name}")
    passed += 1
except Exception as e:
    print(f"❌ [8/8] Telegram Bot — FAILED: {e}")
    failed += 1

# Bonus: Translator
print()
try:
    from deep_translator import GoogleTranslator
    result = GoogleTranslator(source="auto", target="en").translate("नमस्ते")
    print(f"✅ [BONUS] Translator — WORKING | नमस्ते → {result}")
except Exception as e:
    print(f"❌ [BONUS] Translator — FAILED: {e}")

# Summary
print()
print("=" * 55)
print(f"  RESULTS: {passed} passed | {failed} failed | {passed + failed} total")
print("=" * 55)

if failed == 0:
    print("\n  🎯 ALL SYSTEMS GO! Ready to build! 🚀\n")
else:
    print(f"\n  ⚠️  Fix {failed} failed key(s) before proceeding\n")