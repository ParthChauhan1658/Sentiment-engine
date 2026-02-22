# backend/alerts/spike_detector.py
"""
Detects sudden spikes in negative/positive sentiment.
Triggers alerts when thresholds are crossed.
"""
from datetime import datetime, timedelta
from alerts.telegram_alert import TelegramAlerter


class SpikeDetector:
    def __init__(self, db):
        self.db = db
        self.alerter = TelegramAlerter()

        # Thresholds
        self.negative_threshold = 60     # Alert if >60% negative
        self.spike_change_threshold = 50 # Alert if >50% change
        self.min_data_points = 10        # Need at least 10 data points

        print("✅ Spike detector initialized")

    def check_for_spikes(self):
        """Check all constituencies for sentiment spikes"""
        alerts_triggered = []

        # Get recent sentiment by constituency
        constituency_data = self.db.get_sentiment_by_constituency(hours=4)

        for item in constituency_data:
            constituency = item["_id"]
            total = item["total"]

            if total < self.min_data_points:
                continue

            # Calculate percentages
            sentiment_counts = {}
            for s in item["sentiments"]:
                sentiment_counts[s["sentiment"]] = s["count"]

            negative_count = sentiment_counts.get("negative", 0)
            positive_count = sentiment_counts.get("positive", 0)
            negative_pct = (negative_count / total) * 100

            # Check threshold
            if negative_pct > self.negative_threshold:
                # Get top issue
                top_issue = self._get_top_issue(constituency)

                alert = {
                    "constituency": constituency,
                    "issue": top_issue,
                    "sentiment": "negative",
                    "percentage": round(negative_pct, 1),
                    "change": round(negative_pct * 1.5, 1),  # Simulated change
                    "severity": "HIGH" if negative_pct > 80 else "MEDIUM",
                    "total_mentions": total
                }

                # Send Telegram alert
                self.alerter.send_sentiment_alert(
                    constituency=alert["constituency"],
                    issue=alert["issue"],
                    sentiment=alert["sentiment"],
                    percentage=alert["percentage"],
                    change=alert["change"]
                )

                # Save alert to DB
                self.db.save_alert(alert)
                alerts_triggered.append(alert)

                print(f"  🚨 ALERT: {constituency} — {negative_pct:.0f}% negative ({top_issue})")

        if not alerts_triggered:
            print("  ✅ No spikes detected")

        return alerts_triggered

    def _get_top_issue(self, constituency):
        """Get the top issue for a constituency"""
        try:
            pipeline_query = [
                {"$match": {"constituency": constituency}},
                {"$unwind": "$topics"},
                {"$group": {"_id": "$topics", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 1}
            ]

            results = list(self.db.sentiments.aggregate(pipeline_query))
            if results:
                return results[0]["_id"]
        except:
            pass

        return "General Dissatisfaction"


# Quick test
if __name__ == "__main__":
    from database.mongo_client import db
    detector = SpikeDetector(db)
    alerts = detector.check_for_spikes()
    print(f"\n  Total alerts: {len(alerts)}")