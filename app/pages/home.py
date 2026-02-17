import streamlit as st


def app(navigate):

    # HERO SECTION
    col_left, col_right = st.columns([1.4, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div class="fade-in">
                <p class="tag-chip">
                    <span>⚡ Realtime • 82% live accuracy • 98.6% static</span>
                </p>
                <h1 class="hero-title">
                    Indian Sign Language<br/>Translator for everyone.
                </h1>
                <p class="hero-subtitle">
                    Bridge the communication gap between the deaf community and the hearing world
                    using machine learning, computer vision and a smooth experience tailored for ISL.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        cta1, cta2 = st.columns([1, 1])

        with cta1:
            if st.button("🔍 Try Prediction", use_container_width=True):
                navigate("predictSign")

        with cta2:
            if st.button("✍ Create Sign from Text", use_container_width=True):
                navigate("create")

        st.write("")
        st.markdown(
            """
            <span class="pill-btn">
                <span class="icon">💡</span>
                <span>First-of-its-kind ISL-focused experience</span>
            </span>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            """
            <div class="glass-card fade-in">
                <div style="font-size:0.85rem; color:#9ca3af; margin-bottom:0.6rem;">
                    Powered by:
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:0.35rem; margin-bottom:0.9rem;">
                    <span class="tag-chip">🧠 TensorFlow · Keras</span>
                    <span class="tag-chip">📷 OpenCV · cvzone</span>
                    <span class="tag-chip">📊 NumPy · Pandas</span>
                    <span class="tag-chip">☁️ Groq API for language</span>
                </div>
                <hr style="border-color:rgba(55,65,81,0.7); margin:0.6rem 0 0.9rem 0;"/>
                <div style="font-size:0.9rem; color:#e5e7eb; line-height:1.55;">
                    • Upload an image of an ISL gesture and get the predicted character
                    (A–Z and 1–9).<br/><br/>
                    • Convert any phrase into step-by-step ISL instructions with
                    language support for English, Hindi and Marathi.<br/><br/>
                    • Designed to be lightweight, responsive and accessible for demos,
                    classrooms and real use.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # FEATURE GRID
    st.markdown(
        """
        <div class="section-title">What you can do with this app</div>
        <div class="section-subtitle">
            Explore the different modes to understand and create Indian Sign Language.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-grid fade-in">
            <div class="feature-card">
                <div class="feature-card-icon">🔍</div>
                <h4>Predict from Gestures</h4>
                <p>
                    Upload an ISL gesture image and let the model classify it into letters
                    (A–Z) or numbers (1–9). Ideal for testing dataset quality and live demos.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-card-icon">✍</div>
                <h4>Create ISL from Text</h4>
                <p>
                    Type any phrase like <i>“I love India”</i> and get a step-by-step breakdown
                    of how to sign it in Indian Sign Language, powered by Groq.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-card-icon">🌐</div>
                <h4>Multilingual Output</h4>
                <p>
                    Translate recognized characters into English, Hindi or Marathi, making
                    the app more inclusive for different language backgrounds.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
