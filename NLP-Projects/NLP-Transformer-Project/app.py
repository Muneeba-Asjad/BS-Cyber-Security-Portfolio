from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load Fine Tuned Transformer Model
classifier = pipeline(
    "sentiment-analysis",
    model="./models/fine_tuned_model"
)


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    confidence = None
    text = ""

    if request.method == "POST":

        text = request.form["text"]

        if text.strip() != "":
            result = classifier(text)[0]

            prediction = result["label"]
            confidence = round(result["score"] * 100, 2)

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        text=text
    )


if __name__ == "__main__":
    app.run(debug=True)