# summarizer.py

import requests
from transformers import pipeline
from gtts import gTTS
from textblob import TextBlob
import os

# ✅ Summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def fetch_news(company):
    api_key = "034cc0fac4ce41b5b9296bf36f44dc15"
    url = f"https://newsapi.org/v2/everything?q={company}&language=hi&pageSize=2&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return "❌ Failed to fetch news.", []
    data = response.json()
    articles = data.get("articles", [])
    return [{"title": a["title"], "content": a["description"]} for a in articles], []

def summarize_text(text):
    if not text or len(text) < 50:
        return "📜 Text too short for summarization."
    text = text[:1024]
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive 😊"
    elif polarity < 0:
        return "Negative 😞"
    else:
        return "Neutral 😐"

def text_to_speech(text):
    tts = gTTS(text=text, lang="hi")
    if not os.path.exists("assets"):
        os.makedirs("assets")
    filename = "assets/output.mp3"
    tts.save(filename)
    return filename

def process_company_news(company):
    news_data, _ = fetch_news(company)
    if not news_data:
        return "❌ No news articles found.", None

    processed = []
    for article in news_data:
        summary = summarize_text(article["content"])
        sentiment = analyze_sentiment(summary)
        processed.append({
            "Title": article["title"],
            "Summary": summary,
            "Sentiment": sentiment
        })

    full_text = f"{company} की खबरें:\n"
    for r in processed:
        full_text += f"{r['Title']} - {r['Summary']} ({r['Sentiment']})\n"

    audio_path = text_to_speech(full_text)
    return processed, audio_path
