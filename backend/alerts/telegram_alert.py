# backend/alerts/telegram_alert.py
"""
Telegram bot for sending sentiment alerts.
Completely free, unlimited messages.
"""
import requests
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramAlerter:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"

        if self.token and self.chat_id:
            print("✅ Telegram alerter initialized")
        else:
            print("⚠️ Telegram credentials missing — alerts disabled")

    def send_message(self, message):
        """Send a text message via Telegram"""
        if not self.token or not self.chat_id:
            print("  ⚠️ Telegram not configured")
            return False

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()

            if result.get("ok"):
                return True
            else:
                print(f"  ❌ Telegram error: {result.get('description', 'Unknown')}")
                return False

        except Exception as e:
            print(f"  ❌ Telegram failed: {e}")
            return False

    def send_sentiment_alert(self, constituency, issue, sentiment,
                              percentage, change):
        """Send formatted sentiment spike alert"""
        emoji_map = {
            "negative": "🔴",
            "positive": "🟢",
            "neutral": "🟡"
        }

        if change > 200:
            severity, severity_emoji = "HIGH", "🚨"
        elif change > 100:
            severity, severity_emoji = "MEDIUM", "⚠️"
        else:
            severity, severity_emoji = "LOW", "ℹ️"

        message = (
            f"{severity_emoji} <b>SENTIMENT ALERT — {severity}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📍 <b>Constituency:</b> {constituency}\n"
            f"{emoji_map.get(sentiment, '⚪')} <b>Sentiment:</b> {sentiment.upper()}\n"
            f"🔥 <b>Key Issue:</b> {issue}\n"
            f"📊 <b>Percentage:</b> {percentage}% {sentiment}\n"
            f"📈 <b>Change:</b> ↑{change}% in last 2 hours\n"
            f"⏰ <b>Time:</b> {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n\n"
            f"#alert #{constituency.lower().replace(' ', '_')} #{sentiment}"
        )

        return self.send_message(message)

    def send_daily_summary(self, data):
        """Send daily sentiment summary"""
        message = (
            f"📊 <b>DAILY SENTIMENT SUMMARY</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 {datetime.now().strftime('%d %B %Y')}\n\n"
            f"🟢 Positive: {data.get('positive', 0)} mentions\n"
            f"🔴 Negative: {data.get('negative', 0)} mentions\n"
            f"🟡 Neutral: {data.get('neutral', 0)} mentions\n"
            f"📦 Total: {data.get('total', 0)} analyzed\n\n"
            f"🔥 <b>Top Issues:</b>\n"
        )

        for i, topic in enumerate(data.get("top_topics", [])[:5], 1):
            message += f"  {i}. {topic['name']} ({topic['count']} mentions)\n"

        message += f"\n📍 <b>Hotspot:</b> {data.get('hotspot', 'N/A')}\n"
        message += f"\n#daily_summary #sentiment"

        return self.send_message(message)

    def send_startup_message(self):
        """Send message when system starts"""
        message = (
            f"🤖 <b>Sentiment Engine ONLINE</b>\n\n"
            f"⏰ Started: {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
            f"📡 All scrapers active\n"
            f"🧠 NLP models loaded\n"
            f"📊 Dashboard ready\n\n"
            f"System is monitoring political sentiment across India."
        )
        return self.send_message(message)


# Quick test
if __name__ == "__main__":
    alerter = TelegramAlerter()

    print("📤 Sending test messages...\n")

    # Test 1: Basic message
    result = alerter.send_message("🤖 Sentiment Engine Bot is <b>ONLINE</b>! ✅")
    print(f"  Basic message: {'✅ Sent' if result else '❌ Failed'}")

    # Test 2: Sentiment alert
    result = alerter.send_sentiment_alert(
        constituency="Varanasi",
        issue="Water Supply",
        sentiment="negative",
        percentage=78,
        change=340
    )
    print(f"  Sentiment alert: {'✅ Sent' if result else '❌ Failed'}")

    print("\n  Check your Telegram for the messages!")