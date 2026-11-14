from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)

from config import BERT_MODEL

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)

print("Loading model (first time download may take a few minutes)...")
model = AutoModelForSequenceClassification.from_pretrained(BERT_MODEL)

print("Creating sentiment analysis pipeline...")
classifier = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer
)

print("\nModel Loaded Successfully!")


def predict_sentiment(text):
    result = classifier(text)[0]

    return {
        "label": result["label"],
        "confidence": round(result["score"], 4)
    }


if __name__ == "__main__":

    while True:

        text = input("\nEnter Text (type 'exit' to quit): ").strip()

        if text.lower() == "exit":
            print("\nProgram Closed Successfully!")
            break

        if text == "":
            print("Please enter some text.")
            continue

        try:
            prediction = predict_sentiment(text)

            print("\nPrediction")
            print("----------------------------")
            print("Text       :", text)
            print("Label      :", prediction["label"])
            print("Confidence :", prediction["confidence"])

        except Exception as e:
            print("\nError:", e)