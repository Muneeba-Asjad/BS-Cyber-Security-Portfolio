import cv2
import torch
import numpy as np
import streamlit as st

from model import UNet

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Brain Tumor Segmentation",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Brain Tumor Segmentation using U-Net")
st.write("Upload an MRI image to detect the brain tumor region.")

# -----------------------------
# Device
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
st.write("Using Device:", device)

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    model = UNet().to(device)
    model.load_state_dict(
        torch.load(
            "models/unet_model.pth",
            map_location=device
        )
    )
    model.eval()
    return model

model = load_model()

# -----------------------------
# Upload Image
# -----------------------------
uploaded_file = st.file_uploader(
    "Choose MRI Image",
    type=["tif", "png", "jpg", "jpeg"]
)

# -----------------------------
# Prediction
# -----------------------------
if uploaded_file is not None:

    # Don't allow mask image
    if "_mask" in uploaded_file.name.lower():
        st.error("❌ Please upload the MRI image, not the mask image.")
        st.stop()

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        st.error("Unable to read image.")
        st.stop()

    original = image.copy()

    # Resize
    image = cv2.resize(image, (256, 256))

    # Normalize
    image = image.astype(np.float32) / 255.0

    tensor = torch.tensor(
        image,
        dtype=torch.float32
    ).unsqueeze(0).unsqueeze(0).to(device)

    # Prediction
    with torch.no_grad():
        pred = model(tensor)

    pred = pred.cpu().numpy()[0, 0]

    st.subheader("Prediction Statistics")
    st.write(f"Min: {pred.min():.4f}")
    st.write(f"Max: {pred.max():.4f}")
    st.write(f"Mean: {pred.mean():.4f}")

    # Threshold
    mask = (pred > 0.30).astype(np.uint8)

    mask = cv2.resize(
        mask,
        (original.shape[1], original.shape[0]),
        interpolation=cv2.INTER_NEAREST
    )

    # Overlay
    overlay = cv2.cvtColor(
        original,
        cv2.COLOR_GRAY2BGR
    )

    overlay[mask == 1] = [0, 0, 255]

    # -----------------------------
    # Display
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🖼 Original MRI")
        st.image(
            original,
            clamp=True,
            use_container_width=True
        )

    with col2:
        st.subheader("🎯 Predicted Tumor Mask")
        st.image(
            mask * 255,
            clamp=True,
            use_container_width=True
        )

    with col3:
        st.subheader("🔴 Tumor Overlay")
        st.image(
            cv2.cvtColor(
                overlay,
                cv2.COLOR_BGR2RGB
            ),
            use_container_width=True
        )

    if np.sum(mask) > 0:
        st.success("✅ Tumor Detected")
    else:
        st.warning("⚠️ No Tumor Detected")