# backend/api/map_routes.py
from fastapi import APIRouter, Query
from database.mongo_client import db
from geo.constituency_mapper import ConstituencyMapper

router = APIRouter(prefix="/api/map", tags=["Map"])

mapper = ConstituencyMapper()


@router.get("/constituencies")
def get_all_constituencies():
    """Get all constituencies with coordinates"""
    return {"constituencies": mapper.get_all_constituencies()}


@router.get("/heatmap")
def get_heatmap_data(hours: int = Query(24)):
    """Get sentiment data formatted for heatmap"""
    constituency_data = db.get_sentiment_by_constituency(hours=hours)
    coordinates = mapper.get_constituency_coordinates()

    heatmap_points = []

    for item in constituency_data:
        name = item["_id"]
        if name in coordinates:
            coords = coordinates[name]

            # Calculate sentiment score (-1 to +1)
            sentiment_counts = {}
            for s in item["sentiments"]:
                sentiment_counts[s["sentiment"]] = s["count"]

            total = item["total"]
            positive = sentiment_counts.get("positive", 0)
            negative = sentiment_counts.get("negative", 0)

            # Score: -1 (all negative) to +1 (all positive)
            score = (positive - negative) / max(total, 1)

            heatmap_points.append({
                "constituency": name,
                "state": coords["state"],
                "lat": coords["lat"],
                "lng": coords["lng"],
                "score": round(score, 3),
                "total_mentions": total,
                "positive": positive,
                "negative": negative,
                "neutral": sentiment_counts.get("neutral", 0),
                "dominant_sentiment": max(sentiment_counts, key=sentiment_counts.get)
                    if sentiment_counts else "neutral"
            })

    return {"heatmap": heatmap_points}


@router.get("/constituency/{name}")
def get_constituency_detail(name: str, hours: int = Query(24)):
    """Get detailed data for a specific constituency"""
    summary = db.get_sentiment_summary(constituency=name, hours=hours)
    info = mapper.get_constituency_info(name)

    return {
        "constituency": info,
        "sentiment": summary,
        "hours": hours
    }