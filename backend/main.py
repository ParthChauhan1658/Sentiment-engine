# backend/main.py
"""
Sentiment Analysis Engine — FastAPI Server
India Innovates 2026
"""
import os
import re
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from config import validate_config


def _strip_html(text: str) -> str:
    """Remove HTML tags, entities, and URL artifacts from scraped text."""
    if not text:
        return text
    # Remove full anchor tags including content that looks like encoded URLs
    clean = re.sub(r'<a\s[^>]*>.*?</a>', '', text, flags=re.DOTALL)
    # Remove any remaining HTML tags
    clean = re.sub(r'<[^>]+>', ' ', clean)
    # Decode common HTML entities
    clean = re.sub(r'&nbsp;', ' ', clean)
    clean = re.sub(r'&amp;', '&', clean)
    clean = re.sub(r'&lt;', '<', clean)
    clean = re.sub(r'&gt;', '>', clean)
    clean = re.sub(r'&quot;', '"', clean)
    clean = re.sub(r'&#39;', "'", clean)
    clean = re.sub(r'&#\d+;', '', clean)
    # Remove long base64-like strings (from Google News RSS URLs)
    clean = re.sub(r'[A-Za-z0-9_\-]{60,}', '', clean)
    # Collapse whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


_alert_executor = ThreadPoolExecutor(max_workers=1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("\n" + "=" * 55)
    print("  SENTIMENT ANALYSIS ENGINE")
    print("  India Innovates 2026")
    print("=" * 55 + "\n")

    validate_config()

    print("\n  Loading all services (one-time)...")
    from services import Services
    Services.initialize()

    # Share analyzer with sentiment_routes for backward compatibility
    from api import sentiment_routes
    sentiment_routes.analyzer = Services.analyzer

    print("\n  Server ready! Open http://localhost:8000\n")

    yield

    print("\n  Shutting down...")
    _alert_executor.shutdown(wait=False)


app = FastAPI(
    title="Sentiment Analysis Engine",
    description="AI-Driven Multi-Language Political Sentiment Analysis for India",
    version="1.0.0",
    lifespan=lifespan
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -- ROUTES --
from api.dashboard_routes import router as dashboard_router
from api.sentiment_routes import router as sentiment_router
from api.map_routes import router as map_router
from api.alert_routes import router as alert_router

app.include_router(dashboard_router)
app.include_router(sentiment_router)
app.include_router(map_router)
app.include_router(alert_router)


# -- ROOT ENDPOINTS --

@app.get("/")
def root():
    return {
        "name": "Sentiment Analysis Engine",
        "status": "running",
        "version": "1.0.0",
        "hackathon": "India Innovates 2026",
        "docs": "http://localhost:8000/docs"
    }


@app.get("/health")
def health():
    from database.mongo_client import db
    from services import Services
    return {
        "status": "healthy",
        "database": "connected" if db.ping() else "disconnected",
        "services_ready": Services.is_ready(),
        "stats": db.get_stats()
    }


# -- PIPELINE ENDPOINTS (using shared Services) --

def _run_pipeline_sync(keyword_list):
    """Run the full pipeline using shared service instances."""
    from services import Services
    from database.mongo_client import db
    from cache import cache

    raw_data, scrape_stats = Services.scraper_manager.scrape_all(keywords=keyword_list)

    if not raw_data:
        return {"error": "No data scraped", "stats": scrape_stats}

    db.save_raw_data("mixed", raw_data)

    texts = [_strip_html(item["text"]) for item in raw_data if item.get("text")]

    # Pre-detect languages once for all texts
    languages = [Services.translator.detect_language(t) for t in texts]

    sentiment_results = Services.analyzer.analyze_batch(texts, languages=languages)

    # Batch build documents
    batch_docs = []
    constituency_counts = {}

    for i, result in enumerate(sentiment_results):
        raw_item = raw_data[i] if i < len(raw_data) else {}
        language = result.get("language", languages[i] if i < len(languages) else "unknown")

        topics = Services.topic_extractor.extract_topics(result["text"], top_n=3, language=language)
        constituency = Services.mapper.map_text_to_constituency(
            result["text"], raw_item.get("location", "")
        )
        booth = Services.booth_mapper.assign_booth(constituency) if constituency != "unknown" else "unknown"

        constituency_counts[constituency] = constituency_counts.get(constituency, 0) + 1

        batch_docs.append({
            "text": result["text"],
            "source": raw_item.get("source", "unknown"),
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "scores": result.get("scores", {}),
            "language": language,
            "topics": topics,
            "entities": [],
            "constituency": constituency,
            "booth": booth,
            "analyzed_at": datetime.utcnow()
        })

    # Single batch insert instead of N individual inserts
    db.save_sentiments_batch(batch_docs)
    saved_count = len(batch_docs)

    # Invalidate dashboard cache after new data
    cache.invalidate()

    # Check for spikes
    alert_count = 0
    try:
        from alerts.spike_detector import SpikeDetector
        detector = SpikeDetector(db)
        alerts = detector.check_for_spikes()
        alert_count = len(alerts)
    except Exception as e:
        print(f"  Spike detection skipped: {e}")

    # AI summary
    ai_summary = ""
    try:
        summary = db.get_sentiment_summary(hours=1)
        topics_data = db.get_trending_topics(limit=5, hours=1)

        summary_text = f"""
        Total analyzed: {summary['total']}
        Positive: {summary['positive']} ({summary['positive']/max(summary['total'],1)*100:.0f}%)
        Negative: {summary['negative']} ({summary['negative']/max(summary['total'],1)*100:.0f}%)
        Neutral: {summary['neutral']} ({summary['neutral']/max(summary['total'],1)*100:.0f}%)
        Top constituencies: {', '.join(f"{k}({v})" for k, v in list(constituency_counts.items())[:5])}
        Top topics: {', '.join(t['_id'] for t in topics_data[:5]) if topics_data else 'None'}
        """

        ai_summary = Services.summarizer.summarize_sentiments(summary_text)
    except Exception as e:
        print(f"  AI summary skipped: {e}")
        ai_summary = "Summary not available"

    # Non-blocking Telegram notification
    try:
        from alerts.telegram_alert import TelegramAlerter
        alerter = TelegramAlerter()
        summary_data = db.get_sentiment_summary(hours=1)
        topics_data = db.get_trending_topics(limit=5, hours=1)

        _alert_executor.submit(alerter.send_daily_summary, {
            "positive": summary_data["positive"],
            "negative": summary_data["negative"],
            "neutral": summary_data["neutral"],
            "total": summary_data["total"],
            "top_topics": [{"name": t["_id"], "count": t["count"]} for t in topics_data[:5]],
            "hotspot": list(constituency_counts.keys())[0] if constituency_counts else "N/A"
        })
    except Exception as e:
        print(f"  Telegram notification skipped: {e}")

    mapped_count = sum(v for k, v in constituency_counts.items() if k != "unknown")
    total_count = sum(constituency_counts.values())
    mapping_pct = (mapped_count / total_count * 100) if total_count > 0 else 0

    final_summary = db.get_sentiment_summary(hours=1)

    return {
        "success": True,
        "scraped": len(raw_data),
        "analyzed": len(sentiment_results),
        "saved": saved_count,
        "mapped_to_constituency": mapped_count,
        "mapping_percentage": round(mapping_pct, 1),
        "alerts_triggered": alert_count,
        "scrape_stats": scrape_stats,
        "sentiment_summary": final_summary,
        "constituency_distribution": constituency_counts,
        "ai_summary": ai_summary
    }


@app.get("/api/scrape-and-analyze")
def scrape_and_analyze(keywords: str = "Modi government"):
    """Full pipeline: Scrape -> Analyze -> Save -> Return results"""
    keyword_list = [k.strip() for k in keywords.split(",")]
    return _run_pipeline_sync(keyword_list)


@app.get("/api/scrape-source")
def scrape_single_source(source: str = "reddit", keywords: str = "Modi government"):
    """Scrape from a single source"""
    from services import Services
    from database.mongo_client import db
    from cache import cache

    keyword_list = [k.strip() for k in keywords.split(",")]

    data = Services.scraper_manager.scrape_single_source(source, keywords=keyword_list)

    if not data:
        return {"error": f"No data from {source}", "count": 0}

    db.save_raw_data(source, data)

    texts = [_strip_html(item["text"]) for item in data if item.get("text")]
    languages = [Services.translator.detect_language(t) for t in texts]
    results = Services.analyzer.analyze_batch(texts, languages=languages)

    batch_docs = []
    for i, result in enumerate(results):
        raw_item = data[i] if i < len(data) else {}
        language = result.get("language", languages[i] if i < len(languages) else "unknown")
        topics = Services.topic_extractor.extract_topics(result["text"], top_n=3, language=language)
        constituency = Services.mapper.map_text_to_constituency(
            result["text"], raw_item.get("location", "")
        )

        batch_docs.append({
            "text": result["text"],
            "source": source,
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "scores": result.get("scores", {}),
            "language": language,
            "topics": topics,
            "entities": [],
            "constituency": constituency,
            "booth": "unknown",
            "analyzed_at": datetime.utcnow()
        })

    db.save_sentiments_batch(batch_docs)
    cache.invalidate()

    summary = db.get_sentiment_summary(hours=1)

    return {
        "success": True,
        "source": source,
        "scraped": len(data),
        "analyzed": len(results),
        "saved": len(batch_docs),
        "sentiment_summary": summary
    }


@app.get("/api/clear-data")
def clear_all_data():
    """Clear all data — USE ONLY FOR TESTING"""
    from database.mongo_client import db
    from cache import cache
    db.clear_all()
    cache.invalidate()
    return {"message": "All data cleared!", "status": "empty"}


@app.get("/api/clean-html")
def clean_html_in_db():
    """Strip HTML tags, entities, and URL garbage from all stored sentiment text"""
    from database.mongo_client import db
    count = 0
    for doc in db.sentiments.find({"$or": [
        {"text": {"$regex": "<[a-zA-Z].*?>"}},
        {"text": {"$regex": "&nbsp;"}},
        {"text": {"$regex": "[A-Za-z0-9_\\-]{60,}"}},
    ]}):
        clean = _strip_html(doc["text"])
        if clean != doc["text"]:
            db.sentiments.update_one({"_id": doc["_id"]}, {"$set": {"text": clean}})
            count += 1
    return {"cleaned": count}


@app.get("/api/generate-report")
def generate_report(constituency: str = ""):
    """Generate AI report for a constituency or overall"""
    from services import Services
    from database.mongo_client import db

    if constituency:
        summary = db.get_sentiment_summary(constituency=constituency, hours=24)
        report = Services.summarizer.generate_constituency_report(constituency, str(summary))
        return {
            "constituency": constituency,
            "sentiment": summary,
            "report": report
        }
    else:
        summary = db.get_sentiment_summary(hours=24)
        topics = db.get_trending_topics(limit=10, hours=24)
        constituencies = db.get_sentiment_by_constituency(hours=24)

        data_str = f"""
        Overall: {summary}
        Topics: {topics[:5]}
        Constituencies: {constituencies[:5]}
        """

        report = Services.summarizer.summarize_sentiments(data_str)
        return {
            "overall_sentiment": summary,
            "top_topics": topics[:10],
            "constituencies": constituencies[:5],
            "report": report
        }


# -- RUN --

if __name__ == "__main__":
    import uvicorn
    debug = os.getenv("DEBUG", "false").lower() == "true"
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=debug)
