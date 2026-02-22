# backend/database/mongo_client.py
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MONGODB_URI


class Database:
    _instance = None

    def __new__(cls):
        """Singleton — only one database connection"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        try:
            self.client = MongoClient(
                MONGODB_URI,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000
            )
            self.db = self.client["sentimentdb"]

            # Collections
            self.raw_data = self.db["raw_data"]
            self.sentiments = self.db["sentiments"]
            self.topics = self.db["topics"]
            self.alerts = self.db["alerts"]
            self.constituencies = self.db["constituencies"]

            # Test connection
            self.client.admin.command("ping")
            print("✅ MongoDB connected!")
            self._initialized = True

        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            self._initialized = False

    # ── SAVE OPERATIONS ──

    def save_raw_data(self, source, items):
        """Save scraped data from any source"""
        docs = []
        for item in items:
            docs.append({
                "source": source,
                "text": item.get("text", ""),
                "title": item.get("title", ""),
                "author": item.get("author", ""),
                "url": item.get("url", ""),
                "location": item.get("location", ""),
                "language": item.get("language", "unknown"),
                "metadata": item.get("metadata", {}),
                "scraped_at": datetime.utcnow(),
                "processed": False
            })

        if docs:
            result = self.raw_data.insert_many(docs)
            print(f"✅ Saved {len(result.inserted_ids)} items from {source}")
            return result.inserted_ids
        return []

    def save_sentiment(self, data):
        """Save a single processed sentiment result"""
        doc = {
            "text": data["text"],
            "source": data["source"],
            "sentiment": data["sentiment"],
            "confidence": data["confidence"],
            "scores": data.get("scores", {}),
            "language": data.get("language", "en"),
            "topics": data.get("topics", []),
            "entities": data.get("entities", []),
            "constituency": data.get("constituency", "unknown"),
            "booth": data.get("booth", "unknown"),
            "analyzed_at": datetime.utcnow()
        }
        return self.sentiments.insert_one(doc)

    def save_sentiments_batch(self, items):
        """Save multiple sentiment results at once"""
        if items:
            result = self.sentiments.insert_many(items)
            print(f"✅ Saved {len(result.inserted_ids)} sentiment results")
            return result.inserted_ids
        return []

    def save_alert(self, alert_data):
        """Save a triggered alert"""
        alert_data["triggered_at"] = datetime.utcnow()
        alert_data["acknowledged"] = False
        return self.alerts.insert_one(alert_data)

    # ── READ OPERATIONS ──

    def get_unprocessed_data(self, limit=100):
        """Get raw data that hasn't been analyzed yet"""
        return list(
            self.raw_data.find({"processed": False}).limit(limit)
        )

    def mark_as_processed(self, doc_ids):
        """Mark raw data as processed"""
        self.raw_data.update_many(
            {"_id": {"$in": doc_ids}},
            {"$set": {"processed": True}}
        )

    def get_sentiment_summary(self, constituency=None, hours=24):
        """Get sentiment counts for dashboard"""
        match = {
            "analyzed_at": {
                "$gte": datetime.utcnow() - timedelta(hours=hours)
            }
        }
        if constituency:
            match["constituency"] = constituency

        pipeline = [
            {"$match": match},
            {"$group": {
                "_id": "$sentiment",
                "count": {"$sum": 1},
                "avg_confidence": {"$avg": "$confidence"}
            }}
        ]

        results = list(self.sentiments.aggregate(pipeline))
        summary = {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
        for r in results:
            summary[r["_id"]] = r["count"]
            summary["total"] += r["count"]

        return summary

    def get_sentiment_by_constituency(self, hours=24):
        """Get sentiment grouped by constituency"""
        match = {
            "analyzed_at": {
                "$gte": datetime.utcnow() - timedelta(hours=hours)
            },
            "constituency": {"$ne": "unknown"}
        }

        pipeline = [
            {"$match": match},
            {"$group": {
                "_id": {
                    "constituency": "$constituency",
                    "sentiment": "$sentiment"
                },
                "count": {"$sum": 1}
            }},
            {"$group": {
                "_id": "$_id.constituency",
                "sentiments": {
                    "$push": {
                        "sentiment": "$_id.sentiment",
                        "count": "$count"
                    }
                },
                "total": {"$sum": "$count"}
            }},
            {"$sort": {"total": -1}}
        ]

        return list(self.sentiments.aggregate(pipeline))

    def get_trending_topics(self, limit=20, hours=24):
        """Get most mentioned topics"""
        match = {
            "analyzed_at": {
                "$gte": datetime.utcnow() - timedelta(hours=hours)
            }
        }

        pipeline = [
            {"$match": match},
            {"$unwind": "$topics"},
            {"$group": {
                "_id": "$topics",
                "count": {"$sum": 1},
                "avg_sentiment_score": {"$avg": "$confidence"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]

        return list(self.sentiments.aggregate(pipeline))

    def get_sentiment_timeline(self, hours=24, interval_minutes=60):
        """Get sentiment over time for charts"""
        match = {
            "analyzed_at": {
                "$gte": datetime.utcnow() - timedelta(hours=hours)
            }
        }

        pipeline = [
            {"$match": match},
            {"$group": {
                "_id": {
                    "hour": {"$hour": "$analyzed_at"},
                    "day": {"$dayOfMonth": "$analyzed_at"},
                    "sentiment": "$sentiment"
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id.day": 1, "_id.hour": 1}}
        ]

        return list(self.sentiments.aggregate(pipeline))

    def get_source_breakdown(self, hours=24):
        """Get data count by source"""
        match = {
            "analyzed_at": {
                "$gte": datetime.utcnow() - timedelta(hours=hours)
            }
        }

        pipeline = [
            {"$match": match},
            {"$group": {
                "_id": "$source",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]

        return list(self.sentiments.aggregate(pipeline))

    def get_language_distribution(self, hours=24):
        """Get data count by language"""
        match = {
            "analyzed_at": {
                "$gte": datetime.utcnow() - timedelta(hours=hours)
            }
        }

        pipeline = [
            {"$match": match},
            {"$group": {
                "_id": "$language",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]

        return list(self.sentiments.aggregate(pipeline))

    def get_recent_alerts(self, limit=10):
        """Get most recent alerts"""
        return list(
            self.alerts.find()
            .sort("triggered_at", -1)
            .limit(limit)
        )

    def get_recent_sentiments(self, limit=50):
        """Get most recent sentiment results"""
        return list(
            self.sentiments.find(
                {},
                {"_id": 0, "text": 1, "sentiment": 1,
                 "confidence": 1, "source": 1, "language": 1,
                 "constituency": 1, "topics": 1, "analyzed_at": 1}
            )
            .sort("analyzed_at", -1)
            .limit(limit)
        )

    # ── UTILITY ──

    def ping(self):
        """Test connection"""
        try:
            self.client.admin.command("ping")
            return True
        except Exception:
            return False

    def get_stats(self):
        """Get database statistics"""
        return {
            "raw_data_count": self.raw_data.count_documents({}),
            "sentiments_count": self.sentiments.count_documents({}),
            "alerts_count": self.alerts.count_documents({}),
            "unprocessed_count": self.raw_data.count_documents({"processed": False})
        }

    def clear_all(self):
        """Clear all data — USE ONLY FOR TESTING"""
        self.raw_data.delete_many({})
        self.sentiments.delete_many({})
        self.alerts.delete_many({})
        print("⚠️ All data cleared!")


# Singleton instance
db = Database()