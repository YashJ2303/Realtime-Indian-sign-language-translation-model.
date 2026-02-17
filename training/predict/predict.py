# Real-time gesture prediction using webcam
import cv2
import numpy as np
import tensorflow as tf

GESTURES = ["hi", "bye", "yes", "no", "peace", "ok", "stop", "fist", "thumbs_up", "love_you"]
IMG_SIZE = 64

# Load trained model
model = tf.keras.models.load_model("hand_gesture_model.h5")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    roi = frame[100:400, 100:400]
    img = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    gesture = GESTURES[np.argmax(pred)]

    cv2.rectangle(frame, (100,100), (400,400), (0,255,0), 2)
    cv2.putText(frame, gesture, (100, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()