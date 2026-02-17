
# Train the hand gesture recognition model (improved)
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import os

IMG_SIZE = 64
GESTURES = ["hi", "bye", "yes", "no", "peace", "ok", "stop", "fist", "thumbs_up", "love_you"]
NUM_CLASSES = len(GESTURES)
DATASET_PATH = "dataset"

def load_dataset():
    images = []
    labels = []
    class_counts = {g: 0 for g in GESTURES}
    for idx, gesture in enumerate(GESTURES):
        folder = os.path.join(DATASET_PATH, gesture)
        for img_name in os.listdir(folder):
            img_path = os.path.join(folder, img_name)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Warning: Could not read {img_path}, skipping.")
                continue
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            images.append(img)
            labels.append(idx)
            class_counts[gesture] += 1
    print("Class distribution:", class_counts)
    images = np.array(images, dtype=np.float32) / 255.0
    labels = to_categorical(labels, NUM_CLASSES)
    return images, labels

def build_model():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def main():
    images, labels = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42, stratify=labels)

    # Data augmentation
    datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True
    )
    datagen.fit(X_train)

    model = build_model()

    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True),
        ModelCheckpoint('best_hand_gesture_model.h5', save_best_only=True)
    ]

    # Train
    model.fit(
        datagen.flow(X_train, y_train, batch_size=32),
        epochs=20,
        validation_data=(X_test, y_test),
        callbacks=callbacks
    )

    # Save final model
    model.save("hand_gesture_model.h5")
    print("Model saved as hand_gesture_model.h5 (final)")
    print("Best model saved as best_hand_gesture_model.h5")

if __name__ == "__main__":
    main()