# tokenizer.py

from transformers import AutoTokenizer
from config import BERT_MODEL, MAX_LENGTH

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)

def tokenize_text(text):
    encoded = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt"
    )
    return encoded

if __name__ == "__main__":
    sample = "I really enjoyed learning Transformer models."
    output = tokenize_text(sample)

    print("Input IDs:")
    print(output["input_ids"])

    print("\nAttention Mask:")
    print(output["attention_mask"])