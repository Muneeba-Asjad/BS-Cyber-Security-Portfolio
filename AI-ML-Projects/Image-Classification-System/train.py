import os
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from model import create_model

# Create models folder
os.makedirs("models", exist_ok=True)

# Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Normalize images (NO resizing)
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

print("Training Images:", x_train.shape)
print("Testing Images :", x_test.shape)

# Data Augmentation
train_datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)

train_generator = train_datagen.flow(
    x_train,
    y_train,
    batch_size=64
)

# Create Model
model = create_model()

# Callbacks
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True,
    verbose=1
)

checkpoint = ModelCheckpoint(
    "models/best_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

# Train Model
history = model.fit(
    train_generator,
    validation_data=(x_test, y_test),
    epochs=15,
    callbacks=[early_stop, checkpoint]
)

# Evaluate
loss, accuracy = model.evaluate(x_test, y_test, verbose=1)

print("\n==============================")
print(f"Test Accuracy : {accuracy * 100:.2f}%")
print(f"Test Loss     : {loss:.4f}")
print("==============================")

# Save final model
model.save("models/cnn_model.keras")

print("\nTraining Completed Successfully!")