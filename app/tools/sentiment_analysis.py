from transformers import AutoTokenizer, AutoModelForSequenceClassification
import transformers
import torch
import json
import torch.nn.functional as F
from langdetect import detect, DetectorFactory
from .translation import translate_for_sentiment

MODEL_DIR = "app/tools/distilbert_sentiment_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model     = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
DetectorFactory.seed = 0 
model.eval()

idx2label = {0: "negative", 1: "neutral", 2: "positive"}

def predict_sentiment(text: str) -> str:
    """
    Returns one of 'negative' | 'neutral' | 'positive'
    """
    if detect(text) != "en": 
        trans_text = translate_for_sentiment(text)
        if not isinstance(trans_text, dict):
                trans_text = json.loads(trans_text)
        text = trans_text["translated_message"]
    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)
        logits  = outputs.logits     
        probs   = F.softmax(logits, dim=-1)
        pred_id = torch.argmax(probs, dim=-1).item()

    return idx2label[pred_id]