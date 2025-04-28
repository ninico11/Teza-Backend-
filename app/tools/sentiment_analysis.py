from typing import Iterable, List, Tuple
from collections import Counter
from dotenv import load_dotenv
import os
load_dotenv()
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import json
from langdetect import detect, DetectorFactory
from .translation import translate_for_sentiment

MODEL_DIR = os.getenv("MODEL_DIR")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model     = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

DetectorFactory.seed = 0

idx2label = {0: "negative", 1: "neutral", 2: "positive"}

def _ensure_english(text: str) -> str:
    """Translate to English if needed."""
    if detect(text) == "en":
        return text
    trans_text = translate_for_sentiment(text)
    if not isinstance(trans_text, dict):
        trans_text = json.loads(trans_text)
    return trans_text["translated_message"]

def predict_sentiment(text: str) -> str:
    """
    Predict a single sentence (kept for backward-compatibility).
    Returns one of 'negative' | 'neutral' | 'positive'.
    """
    text = _ensure_english(text)

    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt",
    )
    with torch.no_grad():
        logits = model(**inputs).logits
        pred_id = torch.argmax(F.softmax(logits, dim=-1), dim=-1).item()

    return idx2label[pred_id]

def predict_sentiments(
    texts: Iterable[str],
    aggregate: str = "prob"  # or "majority"
) -> Tuple[List[str], str]:

    processed = [_ensure_english(t) for t in texts]

    inputs = tokenizer(
        processed,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt",
    )
    with torch.no_grad():
        logits = model(**inputs).logits
        probs  = F.softmax(logits, dim=-1)          # shape (n, 3)
        pred_ids = torch.argmax(probs, dim=-1).tolist()

    labels = [idx2label[i] for i in pred_ids]

    return labels
