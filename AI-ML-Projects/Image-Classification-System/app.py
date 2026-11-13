import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# -----------------------------
# Page Settings
# -----------------------------
st.set_page_config(
    page_title="Image Classification System",
    page_icon="🖼️"
)

st.title("🖼️ Image Classification System")
st.write("Upload an image and the CNN model will predict its class.")

# -----------------------------
# CIFAR-10 Classes
# -----------------------------
classes = [
    "Airplane",
    "Automobile",
    "Bird",
    "Cat",
    "Deer",
    "Dog",
    "Frog",
    "Horse",
    "Ship",
    "Truck"
]

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_cnn():
    return load_model("models/cnn_model.keras")

model = load_cnn()

# -----------------------------
# Upload Image
# -----------------------------
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Display Original Image
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", width=300)

    # Resize image
    resized = img.resize((32, 32))

    # Convert to array
    img_array = np.array(resized).astype("float32") / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    prediction = model.predict(img_array, verbose=0)[0]

    # Best Prediction
    predicted_index = np.argmax(prediction)
    confidence = prediction[predicted_index] * 100

    st.success(f"Prediction: {classes[predicted_index]}")
    st.info(f"Confidence: {confidence:.2f}%")

    # Top 3 Predictions
    st.subheader("Top 3 Predictions")

    top3 = np.argsort(prediction)[-3:][::-1]

    for i in top3:
        st.write(f"**{classes[i]}** : {prediction[i]*100:.2f}%")

    # All Prediction Scores
    with st.expander("View All Prediction Scores"):
        for i, score in enumerate(prediction):
            st.write(f"{classes[i]} : {score*100:.2f}%")