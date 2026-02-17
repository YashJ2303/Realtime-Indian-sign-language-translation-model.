
import cv2
import os
import numpy as np

# --- CONFIG ---
GESTURES = ["hi", "bye", "yes", "no", "peace", "ok", "stop", "fist", "thumbs_up", "love_you"]
NUM_IMAGES = 200
DATASET_PATH = "dataset"
ROI_SIZE = 300

def ensure_dirs():
    if not os.path.exists(DATASET_PATH):
        os.makedirs(DATASET_PATH)
    for gesture in GESTURES:
        path = os.path.join(DATASET_PATH, gesture)
        if not os.path.exists(path):
            os.makedirs(path)

def augment_and_preprocess(roi):
    """
    Returns a list of augmented/preprocessed images (numpy arrays).
    Includes: original, horizontally flipped, brightness adjusted, normalized.
    """
    images = []
    # Resize to ROI_SIZE x ROI_SIZE
    roi = cv2.resize(roi, (ROI_SIZE, ROI_SIZE))
    # Normalize to [0,255] uint8
    roi = cv2.convertScaleAbs(roi)
    images.append(roi)
    # Horizontal flip
    images.append(cv2.flip(roi, 1))
    # Brightness up
    bright = cv2.convertScaleAbs(roi, alpha=1.0, beta=40)
    images.append(bright)
    # Brightness down
    dark = cv2.convertScaleAbs(roi, alpha=1.0, beta=-40)
    images.append(dark)
    # Optionally, normalize to [0,1] for ML (save as uint8 for now)
    return images

def capture_gesture_images():
    print("\nSign Language Gesture Capture Tool")
    print("Instructions:")
    print("- Press 'c' to capture the current ROI (Region of Interest)")
    print("- Press 'q' to skip to the next gesture")
    print("- Press ESC to exit at any time\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    try:
        for gesture in GESTURES:
            print(f"Collecting images for gesture: {gesture}")
            count = 0
            while count < NUM_IMAGES:
                ret, frame = cap.read()
                if not ret:
                    continue
                frame = cv2.flip(frame, 1)
                h, w, _ = frame.shape
                cx, cy = w // 2, h // 2
                x1 = max(cx - ROI_SIZE//2, 0)
                y1 = max(cy - ROI_SIZE//2, 0)
                x2 = min(cx + ROI_SIZE//2, w)
                y2 = min(cy + ROI_SIZE//2, h)
                roi = frame[y1:y2, x1:x2]
                roi_display = cv2.resize(roi, (ROI_SIZE, ROI_SIZE))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, f"{gesture} - {count}/{NUM_IMAGES}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.putText(frame, "'c': capture, 'q': skip, ESC: exit", (10, h-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                cv2.imshow("Capture Gesture", frame)
                cv2.imshow("ROI", roi_display)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    print("Exiting...")
                    return
                elif key == ord('q'):
                    print(f"Skipping gesture: {gesture}")
                    break
                elif key == ord('c'):
                    # Augment and save all variants
                    aug_imgs = augment_and_preprocess(roi)
                    for aug_idx, img in enumerate(aug_imgs):
                        img_name = os.path.join(DATASET_PATH, gesture, f"{count}_aug{aug_idx}.jpg")
                        cv2.imwrite(img_name, img)
                    count += 1
            print(f"Done with gesture: {gesture}")
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Dataset capture completed!")

if __name__ == "__main__":
    ensure_dirs()
    capture_gesture_images()