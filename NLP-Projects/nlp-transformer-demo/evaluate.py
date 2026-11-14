from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer
)

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix
)

print("Loading Fine-tuned Model...")

model = AutoModelForSequenceClassification.from_pretrained(
    "./models/fine_tuned_model"
)

tokenizer = AutoTokenizer.from_pretrained(
    "./models/fine_tuned_model"
)

print("Loading Dataset...")

dataset = load_dataset("imdb")

test_dataset = dataset["test"].shuffle(seed=42).select(range(200))


def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )


test_dataset = test_dataset.map(tokenize, batched=True)


def compute_metrics(pred):

    labels = pred.label_ids

    predictions = np.argmax(pred.predictions, axis=1)

    accuracy = accuracy_score(labels, predictions)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="binary"
    )

    return {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }


trainer = Trainer(
    model=model,
    compute_metrics=compute_metrics
)

print("\nEvaluating Model...\n")

results = trainer.evaluate(test_dataset)

print("\nEvaluation Results")
print("--------------------------------")
print(f"Accuracy : {results['eval_Accuracy']:.4f}")
print(f"Precision: {results['eval_Precision']:.4f}")
print(f"Recall   : {results['eval_Recall']:.4f}")
print(f"F1 Score : {results['eval_F1 Score']:.4f}")

predictions = trainer.predict(test_dataset)

predicted_labels = np.argmax(predictions.predictions, axis=1)

cm = confusion_matrix(
    test_dataset["label"],
    predicted_labels
)

print("\nConfusion Matrix")
print("--------------------------------")
print(cm)