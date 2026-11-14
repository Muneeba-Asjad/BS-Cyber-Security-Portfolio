import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from datasets import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

print("Loading Dataset...")

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("datasets/dataset.csv")

# Remove unwanted column
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Remove missing values
df = df.dropna()

# Keep only required columns
df = df[["text", "Emotion"]]

# Remove empty text
df = df[df["text"].str.strip() != ""]

# ==========================
# Use only 1000 samples (Fast Training)
# ==========================
df = df.sample(n=1000, random_state=42)

# ==========================
# Encode Labels
# ==========================
label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["Emotion"])

os.makedirs("models", exist_ok=True)

with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("Total Classes:", len(label_encoder.classes_))
print(label_encoder.classes_)

# ==========================
# Train/Test Split (70/30)
# ==========================
train_df, test_df = train_test_split(
    df,
    test_size=0.30,
    random_state=42
)

print("Training Samples:", len(train_df))
print("Testing Samples :", len(test_df))

# ==========================
# Convert to HuggingFace Dataset
# ==========================
train_dataset = Dataset.from_pandas(train_df[["text", "label"]])
test_dataset = Dataset.from_pandas(test_df[["text", "label"]])

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

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

train_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "label"]
)

test_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "label"]
)

print("Loading Model...")

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=len(label_encoder.classes_)
)

# ==========================
# Training Arguments
# ==========================
training_args = TrainingArguments(
    output_dir="./models",
    num_train_epochs=1,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    do_train=True,
    do_eval=True,
    logging_steps=20,
    report_to="none"
)

# ==========================
# Trainer
# ==========================
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