# backend/api/dashboard_routes.py
from fastapi import APIRouter, Query
from database.mongo_client import db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_summary(hours: int = Query(24, description="Hours to look back")):
    """Get overall sentiment summary"""
    summary = db.get_sentiment_summary(hours=hours)
    stats = db.get_stats()

    return {
        "sentiment": summary,
        "stats": stats,
        "hours": hours
    }


@router.get("/timeline")
def get_timeline(hours: int = Query(24)):
    """Get sentiment over time"""
    timeline = db.get_sentiment_timeline(hours=hours)

    # Format for frontend charts
    formatted = []
    for item in timeline:
        formatted.append({
            "hour": item["_id"]["hour"],
            "day": item["_id"]["day"],
            "sentiment": item["_id"]["sentiment"],
            "count": item["count"]
        })

    return {"timeline": formatted}


@router.get("/topics")
def get_trending_topics(limit: int = Query(20), hours: int = Query(24)):
    """Get trending topics"""
    topics = db.get_trending_topics(limit=limit, hours=hours)

    formatted = []
    for t in topics:
        formatted.append({
            "name": t["_id"],
            "count": t["count"]
        })

    return {"topics": formatted}


@router.get("/sources")
def get_source_breakdown(hours: int = Query(24)):
    """Get data count by source"""
    sources = db.get_source_breakdown(hours=hours)

    formatted = []
    for s in sources:
        formatted.append({
            "source": s["_id"],
            "count": s["count"]
        })

    return {"sources": formatted}


@router.get("/languages")
def get_language_distribution(hours: int = Query(24)):
    """Get data count by language"""
    languages = db.get_language_distribution(hours=hours)

    formatted = []
    for l in languages:
        formatted.append({
            "language": l["_id"],
            "count": l["count"]
        })

    return {"languages": formatted}


@router.get("/recent")
def get_recent_sentiments(limit: int = Query(50)):
    """Get most recent sentiment results"""
    results = db.get_recent_sentiments(limit=limit)

    # Convert datetime to string for JSON
    for r in results:
        if "analyzed_at" in r:
            r["analyzed_at"] = r["analyzed_at"].isoformat()

    return {"results": results}


@router.get("/stats")
def get_database_stats():
    """Get database statistics"""
    return db.get_stats()