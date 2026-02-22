# backend/main.py
"""
Sentiment Analysis Engine — FastAPI Server
India Innovates 2026
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import validate_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("\n" + "=" * 55)
    print("  🚀 SENTIMENT ANALYSIS ENGINE")
    print("  India Innovates 2026")
    print("=" * 55 + "\n")

    # Validate API keys
    validate_config()

    # Initialize NLP models (loaded once, shared across requests)
    print("\n🧠 Loading NLP models...")
    from nlp.sentiment import SentimentAnalyzer
    from api import sentiment_routes
    sentiment_routes.analyzer = SentimentAnalyzer()

    print("\n✅ Server ready! Open http://localhost:8000\n")

    yield

    print("\n🛑 Shutting down...")


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

# ── ROUTES ──
from api.dashboard_routes import router as dashboard_router
from api.sentiment_routes import router as sentiment_router
from api.map_routes import router as map_router
from api.alert_routes import router as alert_router

app.include_router(dashboard_router)
app.include_router(sentiment_router)
app.include_router(map_router)
app.include_router(alert_router)


# ── ROOT ENDPOINTS ──

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
    return {
        "status": "healthy",
        "database": "connected" if db.ping() else "disconnected",
        "stats": db.get_stats()
    }


@app.get("/api/scrape-and-analyze")
def scrape_and_analyze(keywords: str = "Modi government"):
    """
    Full pipeline: Scrape → Analyze → Save → Return results
    Use this to populate data!
    """
    from scrapers.scraper_manager import ScraperManager
    from nlp.sentiment import SentimentAnalyzer
    from nlp.topics import TopicExtractor
    from nlp.translator import TranslatorService
    from geo.constituency_mapper import ConstituencyMapper
    from geo.booth_mapper import BoothMapper
    from database.mongo_client import db

    keyword_list = [k.strip() for k in keywords.split(",")]

    # Step 1: Scrape
    print("\n" + "=" * 50)
    print("📡 Step 1: Scraping data...")
    print("=" * 50)
    manager = ScraperManager()
    raw_data, scrape_stats = manager.scrape_all(keywords=keyword_list)

    if not raw_data:
        return {"error": "No data scraped", "stats": scrape_stats}

    # Save raw data
    db.save_raw_data("mixed", raw_data)

    # Step 2: Analyze sentiment
    print("\n" + "=" * 50)
    print("🧠 Step 2: Analyzing sentiment...")
    print("=" * 50)
    analyzer = SentimentAnalyzer()
    texts = [item["text"] for item in raw_data if item.get("text")]
    sentiment_results = analyzer.analyze_batch(texts)

    # Step 3: Extract topics
    print("\n" + "=" * 50)
    print("🏷️ Step 3: Extracting topics...")
    print("=" * 50)
    topic_extractor = TopicExtractor()

    # Step 4: Map to constituencies
    print("\n" + "=" * 50)
    print("📍 Step 4: Mapping to constituencies...")
    print("=" * 50)
    mapper = ConstituencyMapper()
    booth_mapper = BoothMapper()

    # Step 5: Detect languages
    print("\n" + "=" * 50)
    print("🌐 Step 5: Detecting languages...")
    print("=" * 50)
    translator = TranslatorService()

    # Step 6: Combine and save
    print("\n" + "=" * 50)
    print("💾 Step 6: Saving results...")
    print("=" * 50)
    saved_count = 0
    constituency_counts = {}

    for i, result in enumerate(sentiment_results):
        # Find matching raw data
        raw_item = raw_data[i] if i < len(raw_data) else {}

        # Extract topics (translate Hindi first for better topics)
        topics = topic_extractor.extract_topics(result["text"], top_n=3)

        # Map constituency (improved — checks more keywords)
        constituency = mapper.map_text_to_constituency(
            result["text"],
            raw_item.get("location", "")
        )

        # Detect language (improved — catches Hinglish)
        language = translator.detect_language(result["text"])

        # Assign booth if constituency is known
        booth = "unknown"
        if constituency != "unknown":
            booth = booth_mapper.assign_booth(constituency)

        # Track constituency distribution
        constituency_counts[constituency] = constituency_counts.get(constituency, 0) + 1

        # Build final document
        doc = {
            "text": result["text"],
            "source": raw_item.get("source", "unknown"),
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "scores": result.get("scores", {}),
            "language": language,
            "topics": topics,
            "entities": [],
            "constituency": constituency,
            "booth": booth
        }

        db.save_sentiment(doc)
        saved_count += 1

    # Print constituency mapping results
    print("\n📍 Constituency Mapping Results:")
    for c, count in sorted(constituency_counts.items(), key=lambda x: x[1], reverse=True):
        emoji = "✅" if c != "unknown" else "❓"
        print(f"   {emoji} {c}: {count} items")

    mapped_count = sum(v for k, v in constituency_counts.items() if k != "unknown")
    total_count = sum(constituency_counts.values())
    mapping_pct = (mapped_count / total_count * 100) if total_count > 0 else 0
    print(f"\n   📊 Mapped: {mapped_count}/{total_count} ({mapping_pct:.1f}%)")

    # Check for spikes and send alerts
    print("\n" + "=" * 50)
    print("🚨 Step 7: Checking for sentiment spikes...")
    print("=" * 50)
    try:
        from alerts.spike_detector import SpikeDetector
        detector = SpikeDetector(db)
        alerts = detector.check_for_spikes()
        alert_count = len(alerts)
    except Exception as e:
        print(f"   ⚠️ Spike detection skipped: {e}")
        alert_count = 0

    # Generate AI summary
    print("\n" + "=" * 50)
    print("📝 Step 8: Generating AI summary...")
    print("=" * 50)
    ai_summary = ""
    try:
        from nlp.summarizer import Summarizer
        summarizer = Summarizer()

        # Build summary data
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

        ai_summary = summarizer.summarize_sentiments(summary_text)
        print(f"   📝 AI Summary generated!")
    except Exception as e:
        print(f"   ⚠️ AI summary skipped: {e}")
        ai_summary = "Summary not available"

    # Send Telegram notification
    try:
        from alerts.telegram_alert import TelegramAlerter
        alerter = TelegramAlerter()
        
        summary_data = db.get_sentiment_summary(hours=1)
        topics_data = db.get_trending_topics(limit=5, hours=1)
        
        alerter.send_daily_summary({
            "positive": summary_data["positive"],
            "negative": summary_data["negative"],
            "neutral": summary_data["neutral"],
            "total": summary_data["total"],
            "top_topics": [{"name": t["_id"], "count": t["count"]} for t in topics_data[:5]],
            "hotspot": list(constituency_counts.keys())[0] if constituency_counts else "N/A"
        })
        print("   📱 Telegram summary sent!")
    except Exception as e:
        print(f"   ⚠️ Telegram notification skipped: {e}")

    # Final summary
    final_summary = db.get_sentiment_summary(hours=1)

    print("\n" + "=" * 50)
    print("✅ PIPELINE COMPLETE!")
    print("=" * 50)
    print(f"   📡 Scraped: {len(raw_data)} items")
    print(f"   🧠 Analyzed: {len(sentiment_results)} items")
    print(f"   💾 Saved: {saved_count} items")
    print(f"   📍 Mapped: {mapped_count}/{total_count} ({mapping_pct:.1f}%)")
    print(f"   🚨 Alerts: {alert_count}")
    print(f"   😊 Positive: {final_summary['positive']}")
    print(f"   😡 Negative: {final_summary['negative']}")
    print(f"   😐 Neutral: {final_summary['neutral']}")
    print("=" * 50)

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


@app.get("/api/scrape-source")
def scrape_single_source(source: str = "reddit", keywords: str = "Modi government"):
    """Scrape from a single source"""
    from scrapers.scraper_manager import ScraperManager
    from nlp.sentiment import SentimentAnalyzer
    from nlp.topics import TopicExtractor
    from nlp.translator import TranslatorService
    from geo.constituency_mapper import ConstituencyMapper
    from database.mongo_client import db

    keyword_list = [k.strip() for k in keywords.split(",")]

    manager = ScraperManager()
    data = manager.scrape_single_source(source, keywords=keyword_list)

    if not data:
        return {"error": f"No data from {source}", "count": 0}

    # Save raw
    db.save_raw_data(source, data)

    # Analyze
    analyzer = SentimentAnalyzer()
    topic_extractor = TopicExtractor()
    translator = TranslatorService()
    mapper = ConstituencyMapper()

    texts = [item["text"] for item in data if item.get("text")]
    results = analyzer.analyze_batch(texts)

    saved = 0
    for i, result in enumerate(results):
        raw_item = data[i] if i < len(data) else {}
        topics = topic_extractor.extract_topics(result["text"], top_n=3)
        constituency = mapper.map_text_to_constituency(
            result["text"], raw_item.get("location", "")
        )
        language = translator.detect_language(result["text"])

        doc = {
            "text": result["text"],
            "source": source,
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "scores": result.get("scores", {}),
            "language": language,
            "topics": topics,
            "entities": [],
            "constituency": constituency,
            "booth": "unknown"
        }
        db.save_sentiment(doc)
        saved += 1

    summary = db.get_sentiment_summary(hours=1)

    return {
        "success": True,
        "source": source,
        "scraped": len(data),
        "analyzed": len(results),
        "saved": saved,
        "sentiment_summary": summary
    }


@app.get("/api/clear-data")
def clear_all_data():
    """Clear all data — USE ONLY FOR TESTING"""
    from database.mongo_client import db
    db.clear_all()
    return {"message": "All data cleared!", "status": "empty"}


@app.get("/api/generate-report")
def generate_report(constituency: str = ""):
    """Generate AI report for a constituency or overall"""
    from nlp.summarizer import Summarizer
    from database.mongo_client import db

    summarizer = Summarizer()

    if constituency:
        summary = db.get_sentiment_summary(constituency=constituency, hours=24)
        report = summarizer.generate_constituency_report(constituency, str(summary))
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

        report = summarizer.summarize_sentiments(data_str)
        return {
            "overall_sentiment": summary,
            "top_topics": topics[:10],
            "constituencies": constituencies[:5],
            "report": report
        }


# ── RUN ──

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)