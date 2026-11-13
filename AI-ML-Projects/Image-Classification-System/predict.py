import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

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

model = load_model("models/best_model.keras")

img_path = input("Enter image path: ").strip()

if not os.path.isfile(img_path):
    print("Image not found!")
    exit()

img = image.load_img(img_path, target_size=(32, 32))
img = image.img_to_array(img)
img = img.astype("float32") / 255.0
img = np.expand_dims(img, axis=0)

prediction = model.predict(img, verbose=0)

predicted_class = np.argmax(prediction)
confidence = np.max(prediction) * 100

print("\nPrediction :", classes[predicted_class])
print(f"Confidence : {confidence:.2f}%")