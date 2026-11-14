# api.py

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="NLP Transformer API")

classifier = pipeline(
    "sentiment-analysis",
    model="./models"
)

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message":"Transformer NLP API is Running"}

@app.post("/predict")
def predict(data: TextInput):

    result = classifier(data.text)[0]

    return {
        "label": result["label"],
        "confidence": result["score"]
    }