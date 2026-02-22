# backend/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# ── Data Collection ──
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ── AI / LLM ──
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ── Database ──
MONGODB_URI = os.getenv("MONGODB_URI")

# ── Alerts ──
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ── Constants ──
SUPPORTED_LANGUAGES = [
    "hi",   # Hindi
    "en",   # English
    "ta",   # Tamil
    "te",   # Telugu
    "bn",   # Bengali
    "mr",   # Marathi
    "gu",   # Gujarati
    "kn",   # Kannada
    "ml",   # Malayalam
    "pa",   # Punjabi
    "ur",   # Urdu
]

INDIAN_SUBREDDITS = [
    "india",
    "IndiaSpeaks",
    "indianpolitics",
    "delhi",
    "bangalore",
    "mumbai",
    "chennai",
    "kolkata",
    "hyderabad",
]

POLITICAL_KEYWORDS = [
    "Modi", "BJP", "Congress", "AAP",
    "government", "scheme", "election",
    "corruption", "development", "infrastructure",
    "water", "roads", "electricity", "education",
    "healthcare", "employment", "inflation",
    "subsidy", "farmer", "youth",
    "सरकार", "विकास", "भ्रष्टाचार", "चुनाव",
]

SAMPLE_CONSTITUENCIES = [
    {"name": "Varanasi", "state": "Uttar Pradesh", "lat": 25.3176, "lng": 82.9739},
    {"name": "New Delhi", "state": "Delhi", "lat": 28.6139, "lng": 77.2090},
    {"name": "Mumbai North", "state": "Maharashtra", "lat": 19.1176, "lng": 72.8562},
    {"name": "Chennai South", "state": "Tamil Nadu", "lat": 13.0474, "lng": 80.2090},
    {"name": "Kolkata North", "state": "West Bengal", "lat": 22.6051, "lng": 88.3700},
    {"name": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lng": 80.9462},
    {"name": "Patna Sahib", "state": "Bihar", "lat": 25.6093, "lng": 85.1376},
    {"name": "Gandhinagar", "state": "Gujarat", "lat": 23.2156, "lng": 72.6369},
    {"name": "Bangalore South", "state": "Karnataka", "lat": 12.9141, "lng": 77.6411},
    {"name": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lng": 78.4867},
]


def validate_config():
    """Check all required keys are present"""
    required = {
        "YOUTUBE_API_KEY": YOUTUBE_API_KEY,
        "NEWS_API_KEY": NEWS_API_KEY,
        "GROQ_API_KEY": GROQ_API_KEY,
        "MONGODB_URI": MONGODB_URI,
        "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
        "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
    }

    optional = {
        "GEMINI_API_KEY": GEMINI_API_KEY,
    }

    missing_required = [k for k, v in required.items() if not v]
    missing_optional = [k for k, v in optional.items() if not v]

    if missing_required:
        print(f"❌ Missing REQUIRED keys: {', '.join(missing_required)}")
        print("   Please check your .env file")
        return False

    if missing_optional:
        print(f"⚠️  Missing OPTIONAL keys: {', '.join(missing_optional)}")
        print("   (System will work without these)")

    print("✅ All required API keys loaded!")
    return True


if __name__ == "__main__":
    validate_config()