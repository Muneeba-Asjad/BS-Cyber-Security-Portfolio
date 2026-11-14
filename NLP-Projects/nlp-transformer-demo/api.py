from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__, template_folder="../templates")

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    score = None

    if request.method == "POST":
        text = request.form.get("text", "")

        if text.strip():
            result = classifier(text)[0]
            prediction = result["label"]
            score = round(result["score"], 4)

    return render_template(
        "index.html",
        prediction=prediction,
        score=score
    )