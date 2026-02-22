# backend/api/alert_routes.py
from fastapi import APIRouter, Query
from database.mongo_client import db

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("/recent")
def get_recent_alerts(limit: int = Query(10)):
    """Get most recent alerts"""
    alerts = db.get_recent_alerts(limit=limit)

    # Convert ObjectId and datetime for JSON
    formatted = []
    for a in alerts:
        formatted.append({
            "id": str(a.get("_id", "")),
            "constituency": a.get("constituency", ""),
            "issue": a.get("issue", ""),
            "sentiment": a.get("sentiment", ""),
            "percentage": a.get("percentage", 0),
            "change": a.get("change", 0),
            "severity": a.get("severity", ""),
            "triggered_at": a.get("triggered_at", "").isoformat()
                if a.get("triggered_at") else "",
            "acknowledged": a.get("acknowledged", False)
        })

    return {"alerts": formatted}


@router.post("/test")
def trigger_test_alert():
    """Trigger a test alert"""
    from alerts.telegram_alert import TelegramAlerter
    alerter = TelegramAlerter()

    result = alerter.send_sentiment_alert(
        constituency="Varanasi",
        issue="Water Supply (TEST)",
        sentiment="negative",
        percentage=78,
        change=340
    )

    return {
        "sent": result,
        "message": "Test alert sent to Telegram" if result else "Failed to send"
    }