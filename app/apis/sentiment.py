from collections import Counter
from flask import Blueprint, request, jsonify
from ..tools.sentiment_analysis import predict_sentiment, predict_sentiments

sentiment = Blueprint("sentiment", __name__)

@sentiment.route("/predict_sentiment", methods=["POST"])
def predict_sentiment_message():
    data = request.get_json(silent=True)
    if not data or "messages" not in data:
        return jsonify({"error": "POST body must contain a 'messages' field"}), 400

    messages = data["messages"]

    if isinstance(messages, str):
        labels = [predict_sentiment(messages)]
    elif isinstance(messages, (list, tuple)) and all(isinstance(m, str) for m in messages):
        labels = predict_sentiments(messages)
    else:
        return jsonify({"error": "'messages' must be a string or list of strings"}), 400

    counts = Counter(labels)
    total  = len(labels)

    percentages = {
        "positive": round(counts.get("positive", 0) / total * 100, 1),
        "neutral":  round(counts.get("neutral",  0) / total * 100, 1),
        "negative": round(counts.get("negative", 0) / total * 100, 1),
    }
    return jsonify(percentages), 200
