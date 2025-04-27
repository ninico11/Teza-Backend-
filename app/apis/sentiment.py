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
        label = predict_sentiment(messages)
        return jsonify({
            "sentiments": [label],
            "overall_sentiment": label
        }), 200

    if isinstance(messages, (list, tuple)) and all(isinstance(m, str) for m in messages):
        labels, overall = predict_sentiments(messages)  
        return jsonify({
            "sentiments": labels,
            "overall_sentiment": overall
        }), 200

    return jsonify({"error": "'messages' must be a string or list of strings"}), 400
