from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    BatchNormalization,
    Flatten,
    Dense,
    Dropout
)
from tensorflow.keras.optimizers import Adam


def create_model():

    model = Sequential([

        Conv2D(32, (3,3), activation="relu", padding="same",
               input_shape=(32,32,3)),
        BatchNormalization(),
        Conv2D(32, (3,3), activation="relu", padding="same"),
        BatchNormalization(),
        MaxPooling2D(2,2),
        Dropout(0.25),

        Conv2D(64, (3,3), activation="relu", padding="same"),
        BatchNormalization(),
        Conv2D(64, (3,3), activation="relu", padding="same"),
        BatchNormalization(),
        MaxPooling2D(2,2),
        Dropout(0.25),

        Conv2D(128, (3,3), activation="relu", padding="same"),
        BatchNormalization(),
        MaxPooling2D(2,2),
        Dropout(0.25),

        Flatten(),

        Dense(256, activation="relu"),
        Dropout(0.5),

        Dense(10, activation="softmax")
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model