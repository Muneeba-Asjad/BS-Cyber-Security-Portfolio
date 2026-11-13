import streamlit as st
import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

from model import UNet


# ----------------------------
# Device
# ----------------------------
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ----------------------------
# Load Model
# ----------------------------
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


# ----------------------------
# Preprocessing
# ----------------------------
def preprocess_image(image):

    image = np.array(image.convert("L"))

    image = cv2.resize(
        image,
        (256,256)
    )

    image = image.astype(np.float32) / 255.0

    tensor = torch.tensor(image)

    tensor = tensor.unsqueeze(0).unsqueeze(0)

    return tensor.float().to(device)



# ----------------------------
# Prediction
# ----------------------------
def predict(image):

    image_tensor = preprocess_image(image)


    with torch.no_grad():

        prediction = model(image_tensor)

        prediction = torch.sigmoid(prediction)


        st.write("Prediction Statistics")

        st.write(
            "Min:",
            prediction.min().item()
        )

        st.write(
            "Max:",
            prediction.max().item()
        )

        st.write(
            "Mean:",
            prediction.mean().item()
        )


    prediction = prediction.squeeze().cpu().numpy()


    # threshold
    prediction = (
        prediction > 0.1
    ).astype(np.uint8)


    return prediction



# ----------------------------
# Streamlit UI
# ----------------------------

st.title(
    "Brain Tumor Segmentation using UNet"
)


uploaded_file = st.file_uploader(
    "Upload MRI Image",
    type=[
        "png",
        "jpg",
        "jpeg",
        "tif",
        "tiff"
    ]
)


if uploaded_file:


    if "_mask" in uploaded_file.name.lower():

        st.error(
            "Please upload MRI image only, mask file nahi."
        )

        st.stop()



    image = Image.open(uploaded_file)


    st.subheader("Original MRI")

    st.image(
        image,
        width=350
    )



    if st.button("Predict Tumor"):


        mask = predict(image)


        st.subheader(
            "Predicted Tumor Mask"
        )


        fig, ax = plt.subplots()

        ax.imshow(
            mask,
            cmap="gray"
        )

        ax.axis("off")

        st.pyplot(fig)



        # Overlay

        st.subheader(
            "Tumor Overlay"
        )


        img = np.array(
            image.convert("L").resize(
                (256,256)
            )
        )


        fig2, ax2 = plt.subplots()

        ax2.imshow(
            img,
            cmap="gray"
        )

        ax2.imshow(
            mask,
            alpha=0.4
        )

        ax2.axis("off")

        st.pyplot(fig2)