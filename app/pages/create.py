import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_loader_html():
    return """
    <div class="loader-wrapper">
        <div class="loader"></div>
    </div>
    """


def generate_sign_image(text: str):
    return None


def generate_text_steps(text: str) -> str:

    if not GROQ_API_KEY:
        return (
            "ERROR: GROQ_API_KEY is missing.\n\n"
            "Make sure your .env (project root) contains:\n"
            "GROQ_API_KEY=sk-xxxx"
        )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert in Indian Sign Language (ISL). "
                    "For any phrase, break it into individual ISL signs and describe "
                    "clearly how to perform each sign step-by-step. "
                    "Keep it concise, numbered and easy to follow."
                ),
            },
            {
                "role": "user",
                "content": f"Convert this phrase into Indian Sign Language gestures: {text}",
            },
        ],
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        data = res.json()

        if "error" in data:
            return f"ERROR from Groq API: {data['error'].get('message', data['error'])}"

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"ERROR talking to Groq API: {e}"


# ------------------------------
# 3. UI
# ------------------------------
def app(navigate):

    st.markdown(
        """
        <div class="section-title">Create Indian Sign Language from Text</div>
        <div class="section-subtitle">
            Type any sentence and get step-by-step ISL instructions you can practice or teach.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    col_left, col_right = st.columns([1.4, 1], gap="large")

    # LEFT SIDE – just widgets, no HTML wrapper
    with col_left:
        text_input = st.text_area(
            "Enter text to convert into ISL",
            placeholder="For example: I love India",
            height=150,
        )

        st.caption(
            "Tip: Keep sentences short and clear for more precise ISL breakdown."
        )

        generate_btn = st.button("✨ Generate ISL Steps", use_container_width=True)

    # RIGHT SIDE – here we CAN use a single HTML block as a card
    with col_right:
        st.markdown(
            """
            <div class="glass-card-soft fade-in">
                <div class="section-subtitle" style="margin-bottom:0.4rem;">
                    How this works
                </div>
                <ul style="font-size:0.9rem; color:#9ca3af; padding-left:1.1rem; line-height:1.6;">
                    <li>Your text is sent securely to Groq's LLM.</li>
                    <li>The model breaks it down into ISL-friendly chunks.</li>
                    <li>You get numbered, easy-to-follow hand instructions.</li>
                    <li>Use these steps for teaching, practice, or documentation.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # AFTER BUTTON PRESSED
    if generate_btn:

        if not text_input.strip():
            st.error("Please enter some text to convert into ISL.")
            return

        loader = st.empty()
        loader.markdown(get_loader_html(), unsafe_allow_html=True)

        _ = generate_sign_image(text_input)
        steps = generate_text_steps(text_input)

        loader.empty()

        st.write("")
        st.markdown(
            "<div class='section-title'>ISL Step-by-step Instructions</div>",
            unsafe_allow_html=True,
        )

        # This is fine because all content is in ONE HTML block
        st.markdown(
            f"""
            <div class="glass-card fade-in">
                <pre style="
                    white-space:pre-wrap;
                    color:#e5e7eb;
                    font-size:0.95rem;
                    font-family: ui-monospace, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
                    margin:0;
                ">{steps}</pre>
            </div>
            """,
            unsafe_allow_html=True,
        )
