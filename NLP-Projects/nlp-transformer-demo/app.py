from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load model from Hugging Face
classifier = pipeline(
    "sentiment-analysis",
    model="muneeba1/nlp-transformer-demo",
    tokenizer="muneeba1/nlp-transformer-demo"
)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    confidence = None
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if text:
            result = classifier(text)[0]
            prediction = result["label"]
            confidence = f"{result['score'] * 100:.2f}%"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        text=text
    )


if __name__ == "__main__":
    app.run(debug=True)