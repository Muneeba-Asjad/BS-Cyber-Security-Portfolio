from transformers import pipeline

MODEL_PATH = "./models/fine_tuned_model"

classifier = pipeline(
    "text-classification",
    model=MODEL_PATH,
    tokenizer=MODEL_PATH
)

text = input("Enter text: ")

result = classifier(text)

print("\nPrediction:")
print(result)
