import os
import math
import time
import cv2
import numpy as np
import streamlit as st
import tensorflow as tf

from dotenv import load_dotenv
from cvzone.HandTrackingModule import HandDetector
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.optimizers import Adam



# ======================================================
# Config
# ======================================================
MODEL_PATH = "isl_model_new.h5"   # already in your folder
IMG_SIZE = 300
OFFSET = 15

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# ======================================================
# Class Map
# ======================================================
map_characters = {
    0:'1',1:'2',2:'3',3:'4',4:'5',5:'6',6:'7',7:'8',8:'9',
    9:'A',10:'B',11:'C',12:'D',13:'E',14:'F',15:'G',16:'H',17:'I',
    18:'J',19:'K',20:'L',21:'M',22:'N',23:'O',24:'P',25:'Q',26:'R',
    27:'S',28:'T',29:'U',30:'V',31:'W',32:'X',33:'Y',34:'Z'
}

# ======================================================
# Model + Detector singletons
# ======================================================
@st.cache_resource
@st.cache_resource
@st.cache_resource
def get_model():
    adam = Adam(learning_rate=0.00001)
    model = load_model(MODEL_PATH, compile=False)
    model.compile(optimizer=adam, loss="categorical_crossentropy", metrics=["accuracy"])
    return model




@st.cache_resource
def get_camera_and_detector():
    cap = cv2.VideoCapture(0)          # default webcam
    detector = HandDetector(maxHands=2)
    return cap, detector


model = get_model()


# ======================================================
# Preprocessing helpers
# ======================================================
def edge_detection(image):
    blur = cv2.GaussianBlur(image, (5, 5), 2)
    th3 = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2,
    )
    _, res = cv2.threshold(
        th3,
        70,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )
    return res


def preprocess(img):
    """
    img: color image (IMG_SIZE x IMG_SIZE x 3) - composite built from webcam hands
    returns: shaped (1,64,64,1) tensor ready for model
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_edge = edge_detection(img_gray)
    img_resized = cv2.resize(img_edge, (64, 64))
    img_arr = img_to_array(img_resized)
    img_arr = img_arr.reshape(1, 64, 64, 1)
    return img_arr


def predict_image(img):
    pred = model.predict(img)
    pred_class = int(np.argmax(pred))
    label = map_characters.get(pred_class, "?")
    confidence = float(pred[0][pred_class])
    return label, confidence


def place_into_composite(composite, imgResize, x_off, y_off):
    x_off = int(x_off)
    y_off = int(y_off)
    h_comp, w_comp = composite.shape[:2]
    h_src, w_src = imgResize.shape[:2]

    x_end = min(w_comp, x_off + w_src)
    y_end = min(h_comp, y_off + h_src)
    x_start = max(0, x_off)
    y_start = max(0, y_off)

    target_w = x_end - x_start
    target_h = y_end - y_start

    if target_w <= 0 or target_h <= 0:
        return False

    src_x_start = 0 if x_off >= 0 else -x_off
    src_y_start = 0 if y_off >= 0 else -y_off

    src_x_end = min(src_x_start + target_w, w_src)
    src_y_end = min(src_y_start + target_h, h_src)

    src_crop = imgResize[src_y_start:src_y_end, src_x_start:src_x_end]

    if src_crop.shape[0] != target_h or src_crop.shape[1] != target_w:
        target_h = min(target_h, src_crop.shape[0])
        target_w = min(target_w, src_crop.shape[1])
        x_end = x_start + target_w
        y_end = y_start + target_h
        src_crop = src_crop[:target_h, :target_w]

    composite[y_start:y_end, x_start:x_end] = src_crop
    return True


# ======================================================
# One-frame processing for Streamlit loop
# ======================================================
def process_one_frame(cap, detector):
    imgSize = IMG_SIZE
    offset = OFFSET

    success, img = cap.read()
    if not success:
        return None, None, None, None

    # detect hands on original image
    hands, img = detector.findHands(img)  # returns annotated image
    composite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

    if hands:
        hands_sorted = sorted(hands, key=lambda h: h["bbox"][0])
        hands_to_use = hands_sorted[:2]

        if len(hands_to_use) == 1:
            hand = hands_to_use[0]
            x, y, w, h = hand["bbox"]
            x1 = max(x - offset, 0)
            y1 = max(y - offset, 0)
            x2 = min(x + w + offset, img.shape[1])
            y2 = min(y + h + offset, img.shape[0])
            imgCrop = img[y1:y2, x1:x2]

            if imgCrop.size != 0:
                scale = imgSize / max(h, w, 1)
                newW = max(1, math.ceil(w * scale))
                newH = max(1, math.ceil(h * scale))
                newW = min(newW, imgSize)
                newH = min(newH, imgSize)
                try:
                    imgResize = cv2.resize(imgCrop, (newW, newH))
                except Exception:
                    imgResize = None

                if imgResize is not None:
                    xstart = (imgSize - newW) // 2
                    ystart = (imgSize - newH) // 2
                    _ = place_into_composite(composite, imgResize, xstart, ystart)

        else:
            halfW = imgSize // 2
            for idx, hand in enumerate(hands_to_use):
                x, y, w, h = hand["bbox"]
                x1 = max(x - offset, 0)
                y1 = max(y - offset, 0)
                x2 = min(x + w + offset, img.shape[1])
                y2 = min(y + h + offset, img.shape[0])
                imgCrop = img[y1:y2, x1:x2]

                if imgCrop.size == 0:
                    continue

                if h > w:
                    scale = imgSize / max(h, 1)
                    resized_w = max(1, math.ceil(w * scale))
                    resized_h = imgSize
                else:
                    scale = halfW / max(w, 1)
                    resized_w = halfW
                    resized_h = max(1, math.ceil(h * scale))

                resized_w = min(resized_w, halfW)
                resized_h = min(resized_h, imgSize)

                try:
                    imgResize = cv2.resize(imgCrop, (resized_w, resized_h))
                except Exception:
                    imgResize = None

                if imgResize is None:
                    continue

                if idx == 0:
                    x_off = 0 + (halfW - resized_w) // 2
                else:
                    x_off = halfW + (halfW - resized_w) // 2
                y_off = (imgSize - resized_h) // 2

                _ = place_into_composite(composite, imgResize, x_off, y_off)

        # do prediction
        try:
            processed = preprocess(composite)
            label, confidence = predict_image(processed)
        except Exception:
            label, confidence = None, None
    else:
        label, confidence = None, None

    # convert BGR -> RGB for display in Streamlit
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    composite_rgb = cv2.cvtColor(composite, cv2.COLOR_BGR2RGB)

    return img_rgb, composite_rgb, label, confidence


# ======================================================
# Streamlit Page
# ======================================================
def app(navigate):

    # state for webcam loop
    if "realtime_running" not in st.session_state:
        st.session_state.realtime_running = False

    st.markdown(
        """
        <div class="section-title">Realtime ISL Prediction</div>
        <div class="section-subtitle">
            Use your webcam to perform Indian Sign Language gestures and see live predictions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # Start / Stop controls
    ctrl_col1, ctrl_col2, _ = st.columns([1, 1, 3])

    with ctrl_col1:
        if st.button("▶ Start Realtime", use_container_width=True):
            st.session_state.realtime_running = True

    with ctrl_col2:
        if st.button("⏹ Stop", use_container_width=True):
            st.session_state.realtime_running = False

    st.write("")

    # Layout: left = full webcam, right = cropped + output
    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.markdown(
            """
            <div class="realtime-note">
                Live webcam feed. Make sure your hand(s) are clearly visible and well lit.
                For two-hand signs, keep both hands inside the frame.
            </div>
            """,
            unsafe_allow_html=True,
        )
        webcam_placeholder = st.empty()

    with right_col:
        st.markdown(
            """
            <div class="realtime-note">
                Cropped hand region used for the model, plus current prediction.
            </div>
            """,
            unsafe_allow_html=True,
        )
        cropped_placeholder = st.empty()
        output_placeholder = st.empty()

    # If not running, just stop here
    if not st.session_state.realtime_running:
        return

    # If running: grab one frame, show, then rerun
    cap, detector = get_camera_and_detector()
    img_rgb, composite_rgb, label, confidence = process_one_frame(cap, detector)

    if img_rgb is None:
        st.error("Unable to read from webcam. Check camera permissions / connection.")
        st.session_state.realtime_running = False
        return

    webcam_placeholder.image(img_rgb, caption="Webcam - Original", use_column_width=True)
    cropped_placeholder.image(
        composite_rgb,
        caption="Composite / Cropped Hands",
        use_column_width=True,
    )

    if label is not None:
        output_placeholder.markdown(
            f"""
            <div class="glass-card-soft fade-in" style="margin-top:0.4rem;">
                <div style="font-size:0.9rem; color:#9ca3af;">Current prediction</div>
                <div style="font-size:2rem; font-weight:700; margin-top:0.2rem;">
                    {label}
                </div>
                <div style="font-size:0.85rem; color:#9ca3af; margin-top:0.2rem;">
                    Confidence: <b>{confidence*100:.1f}%</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        output_placeholder.markdown(
            """
            <div class="glass-card-soft fade-in" style="margin-top:0.4rem;">
                <div style="font-size:0.9rem; color:#9ca3af;">
                    No hands detected yet. Raise your hand(s) in front of the camera to start.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # small delay to avoid hammering CPU
    time.sleep(0.03)

    # trigger next frame while running
    if st.session_state.realtime_running:
        st.experimental_rerun()
