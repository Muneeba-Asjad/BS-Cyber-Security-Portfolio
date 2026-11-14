from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

print("Loading Dataset...")

dataset = load_dataset("imdb")

print("Loading Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased"
)


def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )


print("Tokenizing Dataset...")

dataset = dataset.map(tokenize, batched=True)

train_dataset = dataset["train"].shuffle(seed=42).select(range(1000))
test_dataset = dataset["test"].shuffle(seed=42).select(range(200))

print("Loading Model...")

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

training_args = TrainingArguments(
    output_dir="./models",
    overwrite_output_dir=True,

    num_train_epochs=1,

    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,

    eval_strategy="epoch",
    save_strategy="epoch",

    logging_steps=50,
    logging_dir="./logs",

    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

print("\nTraining Started...\n")

trainer.train()

print("\nTraining Completed Successfully!")

trainer.save_model("./models/fine_tuned_model")

tokenizer.save_pretrained("./models/fine_tuned_model")

print("Model Saved Successfully!")