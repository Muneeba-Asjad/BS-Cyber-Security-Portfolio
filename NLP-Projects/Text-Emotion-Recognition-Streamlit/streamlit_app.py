import streamlit as st
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from audiorecorder import audiorecorder
import speech_recognition as sr
import tempfile
import os

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="Emotion Recognition AI",
    page_icon="🎭",
    layout="centered"
)

st.title("🎭 Text & Voice Emotion Recognition")
st.write("Enter text or record your voice to detect emotion.")

# -----------------------------------
# Hugging Face Model
# -----------------------------------
MODEL_PATH = "muneeba1/text_emotion_model"

# -----------------------------------
# Load Model
# -----------------------------------
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# -----------------------------------
# Voice to Text
# -----------------------------------
def voice_to_text():
    audio = audiorecorder(
        "🎤 Start Recording",
        "⏹ Stop Recording"
    )

    if len(audio) == 0:
        return ""

    st.audio(audio.export().read(), format="audio/wav")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        audio.export(tmp_file.name, format="wav")
        temp_audio = tmp_file.name

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(temp_audio) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        return text

    except sr.UnknownValueError:
        st.error("❌ Could not understand your voice.")

    except sr.RequestError:
        st.error("❌ Speech Recognition service is unavailable.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

    return ""

# -----------------------------------
# Predict Emotion
# -----------------------------------
def predict_emotion(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = F.softmax(outputs.logits, dim=1)

    prediction = torch.argmax(probabilities, dim=1).item()

    confidence = probabilities[0][prediction].item() * 100

    label = model.config.id2label.get(prediction, f"Class {prediction}")

    return label, confidence

# -----------------------------------
# Input Selection
# -----------------------------------
choice = st.radio(
    "Choose Input",
    ["⌨️ Text Input", "🎤 Voice Input"]
)

text = ""

if choice == "⌨️ Text Input":

    text = st.text_area(
        "Enter your text",
        height=150,
        placeholder="Type something here..."
    )

else:

    voice = voice_to_text()

    if voice:
        st.success("✅ Speech Converted to Text")
        st.write(voice)
        text = voice

# -----------------------------------
# Analyze
# -----------------------------------
if st.button("🔍 Analyze Emotion", use_container_width=True):

    if text.strip():

        emotion, confidence = predict_emotion(text)

        st.success(f"🎭 Emotion : **{emotion}**")
        st.info(f"📊 Confidence : **{confidence:.2f}%**")

    else:

        st.warning("Please enter text or record your voice.")