from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

# Allow the grader/browser to call our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


class SentimentRequest(BaseModel):
    sentences: List[str]


def get_sentiment(sentence: str) -> str:
    """
    Convert a sentence into:
    happy, sad, or neutral
    """

    score = analyzer.polarity_scores(sentence)

    compound = score["compound"]

    # Positive sentiment
    if compound >= 0.05:
        return "happy"

    # Negative sentiment
    elif compound <= -0.05:
        return "sad"

    # Neither clearly positive nor negative
    else:
        return "neutral"


@app.get("/")
def home():
    return {
        "message": "Sentiment API is running"
    }


@app.post("/sentiment")
def sentiment(request: SentimentRequest):

    results = []

    for sentence in request.sentences:

        sentiment_value = get_sentiment(sentence)

        results.append({
            "sentence": sentence,
            "sentiment": sentiment_value
        })

    return {
        "results": results
    }