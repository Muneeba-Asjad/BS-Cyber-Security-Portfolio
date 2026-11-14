from transformers import pipeline

MODEL_PATH = "./models/fine_tuned_model"

print("Loading model...")

classifier = pipeline(
    "text-classification",
    model=MODEL_PATH,
    tokenizer=MODEL_PATH
)

print("Model loaded successfully!")

while True:
    text = input("\nEnter text (or type 'exit' to quit): ")

    if text.lower() == "exit":
        print("Program closed.")
        break

    result = classifier(text)

    print("\nPrediction:")
    print(f"Label : {result[0]['label']}")
    print(f"Score : {result[0]['score']:.4f}")