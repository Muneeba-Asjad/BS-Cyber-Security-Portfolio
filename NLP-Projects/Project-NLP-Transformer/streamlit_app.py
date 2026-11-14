import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="NLP Transformer Demo")

@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="muneeba1/nlp-transformer-demo",
        tokenizer="muneeba1/nlp-transformer-demo",
        token=st.secrets["HF_TOKEN"]
    )

classifier = load_model()

st.title("🤖 NLP Transformer Sentiment Analysis")

text = st.text_area("Enter text")

if st.button("Analyze"):
    if text.strip():
        result = classifier(text)[0]
        st.success(f"Prediction: {result['label']}")
        st.info(f"Confidence: {result['score']*100:.2f}%")