from flask import Blueprint, request, jsonify
import json
from ..tools.sentiment_analysis import predict_sentiment

sentiment = Blueprint('sentiment', __name__)

@sentiment.route('/predict_sentiment', methods=['POST'])
def predict_sentiment_message():
    data = request.get_json()
    content = data.get('message')

    predicted_sentiment = predict_sentiment(content)
    
    return jsonify({
        'sentiment': predicted_sentiment,
    }), 201