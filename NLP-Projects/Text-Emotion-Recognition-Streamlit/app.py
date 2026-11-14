from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pickle

app = Flask(__name__)

# ===========================
# Load Model
# ===========================
MODEL_PATH = "models/fine_tuned_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# Load Label Encoder
with open("models/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    confidence = None
    text = ""

    if request.method == "POST":

        text = request.form.get("text", "").strip()

        if text:

            inputs = tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=128
            )

            with torch.no_grad():
                outputs = model(**inputs)

            probabilities = torch.nn.functional.softmax(
                outputs.logits,
                dim=1
            )

            confidence_score, predicted_class = torch.max(
                probabilities,
                dim=1
            )

            prediction = label_encoder.inverse_transform(
                [predicted_class.item()]
            )[0]

            confidence = f"{confidence_score.item()*100:.2f}%"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        text=text
    )


if __name__ == "__main__":
    app.run(debug=True)