# backend/nlp/summarizer.py
"""
AI-powered summarization and insight generation.
Uses Groq (primary) and Gemini (backup).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GROQ_API_KEY, GEMINI_API_KEY


class Summarizer:
    def __init__(self):
        self.groq_available = False
        self.gemini_available = False

        # Try Groq
        try:
            from groq import Groq
            self.groq_client = Groq(api_key=GROQ_API_KEY)
            self.groq_available = True
            print("✅ Summarizer initialized (Groq)")
        except Exception as e:
            print(f"⚠️ Groq not available: {e}")

        # Try Gemini (NEW package: google-genai)
        try:
            from google import genai
            self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
            self.gemini_available = True
            print("✅ Summarizer backup initialized (Gemini)")
        except Exception as e:
            print(f"⚠️ Gemini not available: {e}")

        if not self.groq_available and not self.gemini_available:
            print("❌ No LLM available! Summarization disabled.")

    def generate(self, prompt, max_tokens=500):
        """Generate text using available LLM"""
        # Try Groq first (faster)
        if self.groq_available:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a political sentiment analyst for India. "
                                       "Give concise, actionable insights. "
                                       "Use bullet points. Be specific."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.3
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"  ⚠️ Groq failed: {e}")

        # Try Gemini as backup (NEW syntax)
        if self.gemini_available:
            try:
                from google import genai
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                return response.text
            except Exception as e:
                print(f"  ⚠️ Gemini failed: {e}")

        return "LLM unavailable. Please check API keys."

    def summarize_sentiments(self, sentiment_data):
        """Generate summary from sentiment data"""
        prompt = f"""Analyze this political sentiment data from India and provide:

1. TOP 3 KEY INSIGHTS (what's the public feeling?)
2. TOP 3 ISSUES of concern
3. RISK AREAS (constituencies/topics with high negative sentiment)
4. RECOMMENDED ACTIONS for political leaders

Data:
{sentiment_data}

Be specific with numbers and constituency names. Keep it under 300 words."""

        return self.generate(prompt)

    def generate_constituency_report(self, constituency, data):
        """Generate report for a specific constituency"""
        prompt = f"""Generate a brief political intelligence report for {constituency} constituency:

Sentiment Data:
{data}

Include:
1. Overall public mood (1 line)
2. Top 3 issues people care about
3. Sentiment trend (improving/declining?)
4. Recommended action for the leader
5. Risk level: HIGH/MEDIUM/LOW

Keep it concise and actionable. Under 200 words."""

        return self.generate(prompt, max_tokens=300)

    def generate_daily_briefing(self, overall_data):
        """Generate daily briefing for dashboard"""
        prompt = f"""Create a brief daily political sentiment briefing for India:

Today's Data:
{overall_data}

Format:
📊 DAILY BRIEFING
- Overall mood: [one line]
- Trending topic: [top issue]
- Hotspot: [most active constituency]
- Alert: [any concerning trend]
- Recommendation: [one action item]

Keep it under 150 words. Be direct."""

        return self.generate(prompt, max_tokens=200)


# Quick test
if __name__ == "__main__":
    summarizer = Summarizer()

    test_data = """
    Varanasi: 65% negative about water supply, 30% positive about new road
    New Delhi: 55% positive about metro expansion, 40% negative about pollution
    Mumbai: 70% negative about flooding, 20% neutral
    Chennai: 60% positive about IT growth, 30% negative about traffic
    """

    print("\n📝 Testing AI Summarization:\n")
    result = summarizer.summarize_sentiments(test_data)
    print(result)