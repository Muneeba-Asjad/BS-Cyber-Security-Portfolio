# model.py

from transformers import AutoModelForSequenceClassification
from config import BERT_MODEL

def load_model():
    model = AutoModelForSequenceClassification.from_pretrained(
        BERT_MODEL,
        num_labels=2
    )
    return model

if __name__ == "__main__":
    model = load_model()
    print(model)