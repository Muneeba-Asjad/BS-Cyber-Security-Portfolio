import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt

from model import UNet

# ----------------------------
# Device
# ----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using Device:", device)

# ----------------------------
# Load Model
# ----------------------------
model = UNet().to(device)

model.load_state_dict(
    torch.load(
        "models/unet_model.pth",
        map_location=device
    )
)

model.eval()

# ----------------------------
# Image Path
# ----------------------------
image_path = r"dataset\kaggle_3m\TCGA_CS_4941_19960909\TCGA_CS_4941_19960909_10.tif"

# ----------------------------
# Read Image
# ----------------------------
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError(f"Image not found: {image_path}")

original = img.copy()

# ----------------------------
# Preprocess
# ----------------------------
img = cv2.resize(img, (256, 256))
img = img.astype(np.float32) / 255.0

tensor = torch.tensor(img).unsqueeze(0).unsqueeze(0).to(device)

# ----------------------------
# Prediction
# ----------------------------
with torch.no_grad():
    pred = model(tensor)

pred = pred.cpu().numpy()[0, 0]

print("Prediction Statistics")
print("---------------------")
print("Min :", pred.min())
print("Max :", pred.max())
print("Mean:", pred.mean())

# ----------------------------
# Threshold
# ----------------------------
mask = (pred > 0.45).astype(np.uint8)

mask = cv2.resize(
    mask,
    (original.shape[1], original.shape[0]),
    interpolation=cv2.INTER_NEAREST
)

# ----------------------------
# Overlay
# ----------------------------
overlay = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
overlay[mask == 1] = [0, 0, 255]   # Red tumor region

# ----------------------------
# Display
# ----------------------------
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.title("Original MRI")
plt.imshow(original, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("Predicted Mask")
plt.imshow(mask, cmap="gray")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title("Tumor Overlay")
plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.tight_layout()
plt.show()