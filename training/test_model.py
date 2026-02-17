import tensorflow as tf
import numpy as np
import cv2

# -----------------------------
# 1. Load your saved model
# -----------------------------
model = tf.keras.models.load_model("isl_model_new.h5")
print("Model loaded successfully!\n")

# -----------------------------
# 2. Image preprocessing function
# -----------------------------
def preprocess_image(path):
    img = cv2.imread(path)

    if img is None:
        raise Exception("Image not found:", path)

    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove lighting differences
    img = cv2.equalizeHist(img)

    # Gaussian blur to suppress background noise
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Resize to match training input
    img = cv2.resize(img, (256, 256))

    # Normalize
    img = img.astype("float32") / 255.0

    # Add dims
    img = np.expand_dims(img, -1)
    img = np.expand_dims(img, 0)

    return img

# -----------------------------
# 3. Run prediction
# -----------------------------
test_image_path = "testC.jpg"  # put your test image here
img = preprocess_image(test_image_path)

# Mapping dictionary based on Train_Set.class_indices
class_map = {
    0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9',
    9: 'A', 10: 'B', 11: 'C', 12: 'D', 13: 'E', 14: 'F', 15: 'G', 16: 'H',
    17: 'I', 18: 'J', 19: 'K', 20: 'L', 21: 'M', 22: 'N', 23: 'O', 24: 'P',
    25: 'Q', 26: 'R', 27: 'S', 28: 'T', 29: 'U', 30: 'V', 31: 'W',
    32: 'X', 33: 'Y', 34: 'Z'
}

pred = model.predict(img)
pred_class = np.argmax(pred)
pred_label = class_map[pred_class]

print("Prediction Class:", pred_class)
print("Prediction Label:", pred_label)

