from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# 1) Load from the saved directory
MODEL_DIR = "app/tools/distilbert_sentiment_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model     = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

# 2) Map prediction indices back to labels
idx2label = {0: "negative", 1: "neutral", 2: "positive"}

def predict_sentiment(text: str) -> str:
    """
    Returns one of 'negative' | 'neutral' | 'positive'
    """
    # Tokenize & prepare
    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )

    # Inference (no grad)
    with torch.no_grad():
        outputs = model(**inputs)
        logits  = outputs.logits          # shape (1, 3)
        probs   = F.softmax(logits, dim=-1)
        pred_id = torch.argmax(probs, dim=-1).item()

    return idx2label[pred_id]