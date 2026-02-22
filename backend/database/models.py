# backend/database/models.py
"""
Data models / schemas for the sentiment engine.
These are dictionary templates — not ORM models.
MongoDB stores them as documents.
"""

from datetime import datetime


def raw_data_model(source, text, title="", author="", url="", 
                   location="", language="unknown", metadata=None):
    """Template for raw scraped data"""
    return {
        "source": source,          # "youtube" | "reddit" | "news" | "twitter"
        "text": text,
        "title": title,
        "author": author,
        "url": url,
        "location": location,
        "language": language,
        "metadata": metadata or {},
        "scraped_at": datetime.utcnow(),
        "processed": False
    }


def sentiment_model(text, source, sentiment, confidence, 
                    language="en", topics=None, entities=None,
                    constituency="unknown", booth="unknown", scores=None):
    """Template for processed sentiment data"""
    return {
        "text": text,
        "source": source,
        "sentiment": sentiment,        # "positive" | "negative" | "neutral"
        "confidence": confidence,      # 0.0 to 1.0
        "scores": scores or {},        # {"positive": 0.8, "negative": 0.1, "neutral": 0.1}
        "language": language,
        "topics": topics or [],        # ["water", "roads", "corruption"]
        "entities": entities or [],    # ["Modi", "BJP", "Varanasi"]
        "constituency": constituency,
        "booth": booth,
        "analyzed_at": datetime.utcnow()
    }


def alert_model(constituency, issue, sentiment, percentage, 
                change, severity="MEDIUM"):
    """Template for triggered alerts"""
    return {
        "constituency": constituency,
        "issue": issue,
        "sentiment": sentiment,
        "percentage": percentage,
        "change": change,             # percentage change in last N hours
        "severity": severity,          # "HIGH" | "MEDIUM" | "LOW"
        "triggered_at": datetime.utcnow(),
        "acknowledged": False
    }


def constituency_model(name, state, lat, lng):
    """Template for constituency data"""
    return {
        "name": name,
        "state": state,
        "lat": lat,
        "lng": lng,
        "total_mentions": 0,
        "positive_count": 0,
        "negative_count": 0,
        "neutral_count": 0,
        "top_issues": [],
        "last_updated": datetime.utcnow()
    }