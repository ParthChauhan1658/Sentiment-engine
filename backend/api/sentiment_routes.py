# backend/api/sentiment_routes.py
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/sentiment", tags=["Sentiment"])

# Will be set from main.py
analyzer = None


class TextInput(BaseModel):
    text: str
    translate_first: Optional[bool] = False


class BatchInput(BaseModel):
    texts: list[str]


@router.post("/analyze")
def analyze_single(input_data: TextInput):
    """Analyze sentiment of a single text"""
    if analyzer is None:
        return {"error": "Analyzer not initialized"}

    result = analyzer.analyze(input_data.text, input_data.translate_first)
    result["input_text"] = input_data.text

    return result


@router.post("/analyze-batch")
def analyze_batch(input_data: BatchInput):
    """Analyze sentiment of multiple texts"""
    if analyzer is None:
        return {"error": "Analyzer not initialized"}

    results = analyzer.analyze_batch(input_data.texts)

    summary = {"positive": 0, "negative": 0, "neutral": 0}
    for r in results:
        summary[r["sentiment"]] += 1

    return {
        "results": results,
        "summary": summary,
        "total": len(results)
    }


@router.get("/test")
def test_sentiment():
    """Quick test with sample texts"""
    if analyzer is None:
        return {"error": "Analyzer not initialized"}

    test_texts = [
        "Modi ji has done great work for the nation",
        "Government is terrible and corrupt",
        "New infrastructure project announced today",
        "मोदी जी ने अच्छा काम किया",
        "सरकार बेकार है"
    ]

    results = []
    for text in test_texts:
        r = analyzer.analyze(text)
        r["input_text"] = text
        results.append(r)

    return {"results": results}