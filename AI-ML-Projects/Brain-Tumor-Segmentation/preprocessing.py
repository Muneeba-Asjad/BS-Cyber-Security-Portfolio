import cv2
import matplotlib.pyplot as plt
import os

# Patient folder
patient_folder = "dataset/kaggle_3m/TCGA_CS_4941_19960909"

# Image number
image_no = 1

image_path = os.path.join(
    patient_folder,
    f"TCGA_CS_4941_19960909_{image_no}.tif"
)

mask_path = os.path.join(
    patient_folder,
    f"TCGA_CS_4941_19960909_{image_no}_mask.tif"
)

# Load image
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Load mask
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

print("Image Shape:", image.shape)
print("Mask Shape :", mask.shape)

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(image, cmap="gray")
plt.title("MRI Image")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(mask, cmap="gray")
plt.title("Tumor Mask")
plt.axis("off")

plt.show()