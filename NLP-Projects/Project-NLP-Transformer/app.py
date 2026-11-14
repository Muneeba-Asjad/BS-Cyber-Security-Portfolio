from flask import Flask, render_template, request

app = Flask(__name__)

positive_words = [
    "good", "great", "excellent", "amazing", "awesome",
    "happy", "love", "best", "fantastic", "nice"
]

negative_words = [
    "bad", "worst", "hate", "terrible", "awful",
    "sad", "poor", "disappointed", "angry", "boring"
]

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    confidence = None
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "").lower().strip()

        if text:
            pos = sum(word in text for word in positive_words)
            neg = sum(word in text for word in negative_words)

            if pos > neg:
                prediction = "POSITIVE"
                confidence = "95%"
            elif neg > pos:
                prediction = "NEGATIVE"
                confidence = "95%"
            else:
                prediction = "NEUTRAL"
                confidence = "50%"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        text=text
    )

if __name__ == "__main__":
    app.run()