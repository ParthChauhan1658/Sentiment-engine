# backend/api/dashboard_routes.py
from fastapi import APIRouter, Query
from database.mongo_client import db
from cache import cache

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_summary(hours: int = Query(24, description="Hours to look back")):
    """Get overall sentiment summary"""
    cache_key = f"summary_{hours}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    summary = db.get_sentiment_summary(hours=hours)
    stats = db.get_stats()

    result = {
        "sentiment": summary,
        "stats": stats,
        "hours": hours
    }
    cache.set(cache_key, result, ttl=30)
    return result


@router.get("/timeline")
def get_timeline(hours: int = Query(24)):
    """Get sentiment over time"""
    cache_key = f"timeline_{hours}"
    cached = cache.get(cache_key)
    if cached:
        return cached

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

    result = {"timeline": formatted}
    cache.set(cache_key, result, ttl=60)
    return result


@router.get("/topics")
def get_trending_topics(limit: int = Query(20), hours: int = Query(24)):
    """Get trending topics"""
    cache_key = f"topics_{limit}_{hours}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    topics = db.get_trending_topics(limit=limit, hours=hours)

    formatted = []
    for t in topics:
        formatted.append({
            "name": t["_id"],
            "count": t["count"]
        })

    result = {"topics": formatted}
    cache.set(cache_key, result, ttl=60)
    return result


@router.get("/sources")
def get_source_breakdown(hours: int = Query(24)):
    """Get data count by source"""
    cache_key = f"sources_{hours}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    sources = db.get_source_breakdown(hours=hours)

    formatted = []
    for s in sources:
        formatted.append({
            "source": s["_id"],
            "count": s["count"]
        })

    result = {"sources": formatted}
    cache.set(cache_key, result, ttl=60)
    return result


@router.get("/languages")
def get_language_distribution(hours: int = Query(24)):
    """Get data count by language"""
    cache_key = f"languages_{hours}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    languages = db.get_language_distribution(hours=hours)

    formatted = []
    for lang in languages:
        formatted.append({
            "language": lang["_id"],
            "count": lang["count"]
        })

    result = {"languages": formatted}
    cache.set(cache_key, result, ttl=60)
    return result


@router.get("/recent")
def get_recent_sentiments(limit: int = Query(50), page: int = Query(1)):
    """Get most recent sentiment results with pagination"""
    skip = (page - 1) * limit
    results = db.get_recent_sentiments(limit=limit, skip=skip)

    # Convert datetime to string for JSON
    for r in results:
        if "analyzed_at" in r:
            r["analyzed_at"] = r["analyzed_at"].isoformat()

    return {"results": results, "page": page, "limit": limit}


@router.get("/stats")
def get_database_stats():
    """Get database statistics"""
    return db.get_stats()
