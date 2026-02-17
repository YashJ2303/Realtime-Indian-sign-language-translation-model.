import streamlit as st
from pages import home, create, predictSign, realtime

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="ISL Translator",
    page_icon="🤟",
    layout="wide"
)


# -----------------------
# GLOBAL THEME / CSS
# -----------------------
def inject_global_css():
    st.markdown(
        """
        <style>
        /* Background + base styles */
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(76, 0, 255, 0.35), transparent 55%),
                radial-gradient(circle at bottom right, rgba(0, 200, 150, 0.35), transparent 55%),
                linear-gradient(135deg, #050816 0%, #020617 40%, #020617 100%);
            color: #f9fafb;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
                         "Segoe UI", sans-serif;
        }

        /* Main content padding so it doesn't hide under fixed navbar */
        .block-container {
            padding-top: 6rem !important;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1200px;
        }

        /* A reusable centered container */
        .center-container {
            max-width: 1200px;
            margin: 0 auto;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* Top nav */
        .top-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            backdrop-filter: blur(18px);
            background: rgba(10, 10, 25, 0.85);
            border-bottom: 1px solid rgba(148, 163, 184, 0.25);
        }

        .top-nav-inner {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0.6rem 2.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            font-weight: 600;
            font-size: 1.05rem;
            letter-spacing: 0.04em;
        }

        .brand-icon {
            font-size: 1.35rem;
        }

        .brand span {
            color: #e5e7eb;
        }

        .brand-sub {
            font-size: 0.72rem;
            color: #9ca3af;
        }

        /* Nav pills row */
        .nav-pills {
            display: flex;
            gap: 0.4rem;
            align-items: center;
            justify-content: center;
            margin-top: 0.25rem;
        }

        .nav-pill {
            padding: 0.2rem 0.9rem;
            font-size: 0.8rem;
            border-radius: 999px;
            border: 1px solid transparent;
            color: #9ca3af;
            background: rgba(15, 23, 42, 0.7);
        }

        .nav-pill.active {
            color: #e5e7eb;
            border-color: rgba(96, 165, 250, 0.8);
            background: radial-gradient(circle at top left,
                        rgba(59, 130, 246, 0.35),
                        rgba(15, 23, 42, 0.95));
            box-shadow: 0 0 18px rgba(59, 130, 246, 0.3);
        }

        /* Global glass card */
        .glass-card {
            background: linear-gradient(135deg,
                        rgba(15, 23, 42, 0.93),
                        rgba(15, 23, 42, 0.75));
            border-radius: 1.3rem;
            border: 1px solid rgba(148, 163, 184, 0.35);
            box-shadow:
                0 18px 45px rgba(15, 23, 42, 0.9),
                0 0 0 1px rgba(15, 23, 42, 1);
            padding: 1.4rem 1.5rem;
        }

        .glass-card-soft {
            background: linear-gradient(140deg,
                        rgba(15, 23, 42, 0.85),
                        rgba(15, 23, 42, 0.65));
            border-radius: 1.1rem;
            border: 1px solid rgba(75, 85, 99, 0.5);
            padding: 1rem 1.2rem;
        }

        /* Headings */
        h1, h2, h3 {
            font-weight: 700 !important;
            letter-spacing: 0.02em;
        }

        .hero-title {
            font-size: clamp(2.4rem, 3vw, 3.1rem);
            font-weight: 800;
            line-height: 1.12;
            background: linear-gradient(120deg, #e5e7eb, #93c5fd, #a5b4fc);
            -webkit-background-clip: text;
            color: transparent;
        }

        .hero-subtitle {
            margin-top: 0.8rem;
            color: #9ca3af;
            font-size: 0.98rem;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 600;
            margin-bottom: 0.3rem;
        }

        .section-subtitle {
            color: #9ca3af;
            font-size: 0.9rem;
        }

        /* Primary buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #4f46e5, #0ea5e9);
            color: #f9fafb;
            border-radius: 999px;
            border: 0;
            padding: 0.45rem 1.2rem;
            font-weight: 600;
            font-size: 0.9rem;
            letter-spacing: 0.03em;
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.8);
            width: 100%;
            transition:
                transform 120ms ease-out,
                box-shadow 120ms ease-out,
                filter 120ms ease-out;
        }

        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.95);
            filter: brightness(1.05);
        }

        div.stButton > button:focus {
            outline: 2px solid rgba(96, 165, 250, 0.9);
            outline-offset: 2px;
        }

        /* Secondary pill buttons (for small actions) */
        .pill-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.4);
            font-size: 0.78rem;
            color: #9ca3af;
            background: rgba(15, 23, 42, 0.8);
        }

        .pill-btn span.icon {
            font-size: 0.85rem;
        }

        /* Text area */
        div[data-testid="stTextArea"] textarea {
            background: radial-gradient(circle at top left,
                        rgba(59, 130, 246, 0.18),
                        rgba(15, 23, 42, 0.95));
            border-radius: 1rem;
            border: 1px solid rgba(148, 163, 184, 0.55);
            color: #e5e7eb;
            min-height: 140px;
        }

        /* File uploader */
        div[data-testid="stFileUploader"] {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 1.1rem;
            padding: 0.9rem 0.9rem 1.1rem 0.9rem;
            border: 1px dashed rgba(148, 163, 184, 0.7);
        }

        div[data-testid="stFileUploader"] section {
            text-align: center;
        }

        /* Text area label */
        div[data-testid="stTextArea"] label {
            font-size: 0.82rem;
            color: #9ca3af;
        }

        /* Read aloud row */
        .read-aloud {
            margin-top: 0.4rem;
            font-size: 0.9rem;
            color: #9ca3af;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }

        .read-aloud span.icon {
            font-size: 1.05rem;
        }

        /* Small tag chips */
        .tag-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            border-radius: 999px;
            border: 1px solid rgba(55, 65, 81, 0.9);
            padding: 0.18rem 0.6rem;
            font-size: 0.72rem;
            color: #9ca3af;
            background: rgba(15, 23, 42, 0.95);
        }

        /* Feature cards on home page */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 1.1rem;
            margin-top: 1.4rem;
        }

        .feature-card {
            background: linear-gradient(135deg,
                        rgba(15, 23, 42, 0.96),
                        rgba(15, 23, 42, 0.8));
            border-radius: 1.1rem;
            border: 1px solid rgba(75, 85, 99, 0.7);
            padding: 1rem 1.1rem;
            font-size: 0.9rem;
        }

        .feature-card h4 {
            font-size: 1rem;
            margin-bottom: 0.25rem;
        }

        .feature-card-icon {
            font-size: 1.25rem;
            margin-bottom: 0.3rem;
        }

        /* Subtle fade-in */
        .fade-in {
            animation: fadeInUp 0.4s ease-out;
        }

        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(6px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* Loader (buffer animation) */
        .loader-wrapper {
            display: flex;
            justify-content: center;
            margin-top: 0.6rem;
            margin-bottom: 0.2rem;
        }

        .loader {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            border: 3px solid rgba(148, 163, 184, 0.5);
            border-top-color: #60a5fa;
            animation: spin 0.85s linear infinite;
        }

        .card {
            background: ...; /* same as glass-card */
            border-radius: 1.3rem;
            padding: 1.5rem;
            border: 1px solid rgba(148,163,184,0.35);
        }

        /* Realtime page helpers */
        .realtime-note {
            font-size: 0.85rem;
            color: #9ca3af;
            margin-bottom: 0.4rem;
        }

        div[data-testid="stImage"] img {
            border-radius: 1rem;
            border: 1px solid rgba(148, 163, 184, 0.35);
        }


        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_global_css()


# -----------------------
# NAVIGATION STATE
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"


def navigate(page: str):
    st.session_state.page = page


# -----------------------
# TOP NAVBAR
# -----------------------
with st.container():
    st.markdown(
        """
        <div class="top-nav">
            <div class="top-nav-inner">
                <div class="brand">
                    <span class="brand-icon">🤟</span>
                    <div>
                        <span>ISL Translator</span><br/>
                        <span class="brand-sub">Real-time Indian Sign Language assistant</span>
                    </div>
                </div>
                <div class="brand-sub">
                    Built with ML & Computer Vision
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")  # spacer so content does not hide behind fixed nav
st.write("")  # extra spacer


# -----------------------
# NAV BUTTONS + PILLS (centered)
# -----------------------
st.markdown('<div class="center-container">', unsafe_allow_html=True)

nav_cols = st.columns(4)

with nav_cols[0]:
    if st.button("🏠 Home", use_container_width=True):
        navigate("home")

with nav_cols[1]:
    if st.button("✍ Create Sign", use_container_width=True):
        navigate("create")

with nav_cols[2]:
    if st.button("🔍 Predict Sign", use_container_width=True):
        navigate("predictSign")

with nav_cols[3]:
    if st.button("📹 Realtime Prediction", use_container_width=True):
        navigate("realtime")

st.markdown(
    f"""
    <div class="nav-pills" style="justify-content:center;">
        <span class="nav-pill {'active' if st.session_state.page=='home' else ''}">
            Home
        </span>
        <span class="nav-pill {'active' if st.session_state.page=='create' else ''}">
            Create ISL from Text
        </span>
        <span class="nav-pill {'active' if st.session_state.page=='predictSign' else ''}">
            Predict from Image
        </span>
        <span class="nav-pill {'active' if st.session_state.page=='realtime' else ''}">
            Realtime Prediction
        </span>

    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)


st.write("")  # small spacer

# -----------------------
# ROUTER
# -----------------------
if st.session_state.page == "home":
    home.app(navigate)

elif st.session_state.page == "create":
    create.app(navigate)

elif st.session_state.page == "predictSign":
    predictSign.app(navigate)

elif st.session_state.page == "realtime":
    realtime.app(navigate)

else:
    st.error("Page not found.")
