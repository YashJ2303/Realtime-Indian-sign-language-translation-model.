import os
import tempfile

import cv2
import numpy as np
import requests
import streamlit as st
import tensorflow as tf
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_loader_html():
    return """
    <div class="loader-wrapper">
        <div class="loader"></div>
    </div>
    """


@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("isl_model.h5")
    return model


model = load_model()


def preprocess_image(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    img = cv2.imread(tmp_path)
    if img is None:
        raise Exception("Image not found or cannot open.")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.resize(img, (256, 256))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, -1)
    img = np.expand_dims(img, 0)

    return img


class_map = {
    0: "1",
    1: "2",
    2: "3",
    3: "4",
    4: "5",
    5: "6",
    6: "7",
    7: "8",
    8: "9",
    9: "A",
    10: "B",
    11: "C",
    12: "D",
    13: "E",
    14: "F",
    15: "G",
    16: "H",
    17: "I",
    18: "J",
    19: "K",
    20: "L",
    21: "M",
    22: "N",
    23: "O",
    24: "P",
    25: "Q",
    26: "R",
    27: "S",
    28: "T",
    29: "U",
    30: "V",
    31: "W",
    32: "X",
    33: "Y",
    34: "Z",
}


def translate_text(text, target_lang):
    if target_lang == "English":
        return text

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": f"Translate this to {target_lang}."},
            {"role": "user", "content": text},
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=payload,
        headers=headers,
    )

    try:
        return res.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Translation Error"


def app(navigate):

    st.markdown(
        """
        <div class="section-title">Predict Indian Sign Language from Image</div>
        <div class="section-subtitle">
            Upload an ISL gesture image and get the predicted character in your preferred language.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    col_left, col_right = st.columns([1.1, 1], gap="large")

    # LEFT – plain widgets (no HTML wrapper)
    with col_left:
        st.subheader("Prediction Settings", anchor=False)

        prediction_mode = st.selectbox(
            "What do you want to predict?",
            ["Letters (A–Z / 1–9)", "Gesture (Coming Soon)"],
        )

        lang = st.selectbox(
            "Output Language",
            ["English", "Hindi", "Marathi"],
        )

        st.caption("Translations are handled automatically using Groq.")
        st.write("")

        file = st.file_uploader(
            "Upload an ISL gesture image",
            type=["jpg", "jpeg", "png"],
        )

        if file is not None:
            st.image(file, caption="Uploaded Image", width=260)

    # RIGHT – output
    with col_right:
        st.subheader("Model Output", anchor=False)

        output_box = st.empty()
        extra_info_box = st.empty()

        if file is not None:

            if prediction_mode == "Letters (A–Z / 1–9)":
                try:
                    img = preprocess_image(file)

                    loader = st.empty()
                    loader.markdown(get_loader_html(), unsafe_allow_html=True)

                    pred = model.predict(img)[0]

                    loader.empty()

                    pred_class = int(np.argmax(pred))
                    predicted_letter = class_map.get(pred_class, "?")
                    confidence = float(pred[pred_class]) * 100.0

                    result_text = translate_text(predicted_letter, lang)

                    output_box.text_area(
                        "Predicted Output",
                        result_text,
                        height=120,
                    )

                    extra_info_box.markdown(
                        f"""
                        <div style="margin-top:0.6rem; font-size:0.9rem; color:#9ca3af;">
                            Raw prediction: <b>{predicted_letter}</b><br/>
                            Estimated confidence: <b>{confidence:.2f}%</b>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                except Exception as e:
                    output_box.text_area(
                        "Predicted Output",
                        "",
                        height=120,
                    )
                    extra_info_box.error(f"Error while processing image: {e}")

            else:
                output_box.text_area(
                    "Predicted Output",
                    "Gesture prediction model coming soon.",
                    height=120,
                )

        else:
            output_box.text_area(
                "Predicted Output",
                "",
                placeholder="Upload an image to get prediction...",
                height=120,
            )

        st.markdown(
            """
            <div class="read-aloud">
                <span class="icon">🔊</span>
                <span>Read aloud (future enhancement)</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
