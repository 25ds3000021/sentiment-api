from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

# Allow the IITM grader/browser to access our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: List[str]


# Words that usually indicate happiness / positive sentiment
happy_words = {
    "love", "loved", "loving",
    "like", "liked",
    "happy", "happier", "happiest",
    "great", "good", "excellent", "amazing",
    "awesome", "wonderful", "fantastic",
    "perfect", "best", "beautiful",
    "enjoy", "enjoyed", "enjoying",
    "excited", "exciting",
    "glad", "delighted", "pleased",
    "nice", "brilliant", "superb",
    "success", "successful",
    "fun", "smile", "smiling",
    "thankful", "grateful",
    "favorite", "favourite",
    "impressive"
}


# Words that usually indicate sadness / negative sentiment
sad_words = {
    "sad", "sadly", "unhappy",
    "hate", "hated",
    "bad", "terrible", "awful",
    "horrible", "worst", "poor",
    "disappointed", "disappointing",
    "angry", "upset", "annoyed",
    "frustrated", "frustrating",
    "pain", "painful",
    "cry", "crying",
    "broken", "failure", "failed",
    "fail", "problem", "problems",
    "worry", "worried",
    "unfortunately", "miserable",
    "disaster", "useless",
    "boring", "regret"
}


def get_sentiment(sentence: str) -> str:
    # Convert sentence to lowercase
    text = sentence.lower()

    # Extract words only
    words = re.findall(r"\b[\w']+\b", text)

    happy_score = 0
    sad_score = 0

    for word in words:
        if word in happy_words:
            happy_score += 1

        if word in sad_words:
            sad_score += 1

    # Some common phrases
    positive_phrases = [
        "very good",
        "so good",
        "really good",
        "very happy",
        "so happy",
        "really happy",
        "thank you",
        "well done",
        "looking forward",
        "highly recommend"
    ]

    negative_phrases = [
        "very bad",
        "so bad",
        "really bad",
        "not good",
        "not happy",
        "don't like",
        "do not like",
        "not satisfied",
        "very disappointed",
        "never again"
    ]

    for phrase in positive_phrases:
        if phrase in text:
            happy_score += 2

    for phrase in negative_phrases:
        if phrase in text:
            sad_score += 2

    # Handle simple negation
    if "not good" in text or "not great" in text or "not happy" in text:
        sad_score += 2

    if "not bad" in text:
        happy_score += 1

    # Decide final sentiment
    if happy_score > sad_score:
        return "happy"

    elif sad_score > happy_score:
        return "sad"

    else:
        return "neutral"


@app.get("/")
def home():
    return {"message": "Sentiment API is running"}


@app.post("/sentiment")
def sentiment(request: SentimentRequest):

    results = []

    for sentence in request.sentences:
        sentiment_value = get_sentiment(sentence)

        results.append({
            "sentence": sentence,
            "sentiment": sentiment_value
        })

    return {"results": results}