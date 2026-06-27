import streamlit as st
import requests
import random
import time
from PIL import Image
import io

st.set_page_config(
    page_title="AI Magic Art Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: linear-gradient(160deg, #ffecd2 0%, #fcb69f 25%, #ffeaa7 50%, #dfe6e9 75%, #c7ecee 100%);
    background-attachment: fixed;
    font-family: 'Nunito', sans-serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff9f0, #ffecd2) !important;
    border-right: 3px dashed #fab1a0 !important;
}

section[data-testid="stSidebar"] * {
    font-family: 'Nunito', sans-serif !important;
}

/* Floating stars background */
.stApp::before {
    content: "✦ ✧ ★ ✦ ✧ ★ ✦ ✧ ★ ✦";
    position: fixed;
    top: 10px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 20px;
    color: #fdcb6e;
    opacity: 0.4;
    pointer-events: none;
    animation: floatStars 6s ease-in-out infinite;
    z-index: 0;
}

@keyframes floatStars {
    0%, 100% { transform: translateY(0px); opacity: 0.4; }
    50% { transform: translateY(-10px); opacity: 0.7; }
}

/* Main header */
.magic-header {
    text-align: center;
    padding: 36px 24px 28px;
    background: white;
    border-radius: 32px;
    border: 4px solid #fdcb6e;
    box-shadow: 0 8px 0 #e17055, 0 12px 24px rgba(0,0,0,0.1);
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.magic-header::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, #fff9f0 0%, #ffffff 100%);
    z-index: 0;
}

.magic-header > * { position: relative; z-index: 1; }

.magic-header h1 {
    font-family: 'Fredoka One', cursive;
    font-size: 42px;
    color: #e17055;
    letter-spacing: 1px;
    line-height: 1.2;
    margin-bottom: 8px;
    animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

.magic-header p {
    color: #b2bec3;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.magic-header .stars-row {
    font-size: 28px;
    margin-bottom: 10px;
    animation: spin-stars 4s linear infinite;
}

@keyframes spin-stars {
    0% { letter-spacing: 2px; }
    50% { letter-spacing: 8px; }
    100% { letter-spacing: 2px; }
}

/* Sidebar labels */
label, .gr-label {
    font-family: 'Fredoka One', cursive !important;
    font-size: 15px !important;
    color: #e17055 !important;
    letter-spacing: 0.5px !important;
    text-transform: none !important;
}

/* Input fields */
textarea, input[type="text"], input[type="password"] {
    background: #fff9f0 !important;
    border: 2px solid #fab1a0 !important;
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 14px !important;
    color: #2d3436 !important;
    padding: 10px 14px !important;
}

textarea:focus, input:focus {
    border-color: #e17055 !important;
    box-shadow: 0 0 0 3px #fdcb6e44 !important;
}

/* Generate button */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #e17055, #d63031);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 16px;
    font-family: 'Fredoka One', cursive;
    font-size: 20px;
    letter-spacing: 1px;
    cursor: pointer;
    box-shadow: 0 6px 0 #b71c1c, 0 8px 16px rgba(211,63,41,0.3);
    transform: translateY(0);
    transition: all 0.15s ease;
    margin-top: 8px;
}

div.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 0 #b71c1c, 0 12px 20px rgba(211,63,41,0.35);
}

div.stButton > button:active {
    transform: translateY(4px);
    box-shadow: 0 2px 0 #b71c1c;
}

/* Download button */
div.stDownloadButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00b894, #00cec9);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 12px;
    font-family: 'Fredoka One', cursive;
    font-size: 17px;
    box-shadow: 0 5px 0 #00695c;
    transition: all 0.15s ease;
    margin-top: 10px;
}

div.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 0 #00695c;
}

/* Result card */
.result-card {
    background: white;
    border-radius: 28px;
    border: 3px solid #fdcb6e;
    box-shadow: 0 8px 0 #e17055, 0 12px 32px rgba(0,0,0,0.08);
    padding: 24px;
    margin-top: 8px;
}

.result-card h3 {
    font-family: 'Fredoka One', cursive;
    color: #e17055;
    font-size: 22px;
    margin-bottom: 16px;
    text-align: center;
}

/* Info rows */
.info-pill {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #fff9f0;
    border: 2px solid #ffecd2;
    border-radius: 50px;
    padding: 8px 16px;
    margin-bottom: 8px;
}

.info-pill-label {
    font-family: 'Fredoka One', cursive;
    color: #e17055;
    font-size: 13px;
    min-width: 90px;
}

.info-pill-value {
    color: #2d3436;
    font-size: 13px;
    font-weight: 700;
}

/* Verified badge */
.verified-badge {
    text-align: center;
    background: linear-gradient(135deg, #55efc4, #00b894);
    color: white;
    border-radius: 50px;
    padding: 8px 20px;
    font-family: 'Fredoka One', cursive;
    font-size: 15px;
    margin-top: 12px;
    box-shadow: 0 4px 0 #00695c;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 60px 30px;
    background: white;
    border-radius: 32px;
    border: 3px dashed #fab1a0;
    margin-top: 8px;
}

.empty-state .big-emoji {
    font-size: 72px;
    animation: wiggle 2s ease-in-out infinite;
    display: block;
    margin-bottom: 16px;
}

@keyframes wiggle {
    0%, 100% { transform: rotate(-5deg); }
    50% { transform: rotate(5deg); }
}

.empty-state h3 {
    font-family: 'Fredoka One', cursive;
    color: #e17055;
    font-size: 24px;
    margin-bottom: 8px;
}

.empty-state p {
    color: #b2bec3;
    font-size: 15px;
    font-weight: 600;
}

/* Sidebar decoration */
.sidebar-mascot {
    text-align: center;
    font-size: 48px;
    margin: 8px 0 16px 0;
    animation: bounce 2s ease-in-out infinite;
}

.sidebar-title {
    font-family: 'Fredoka One', cursive;
    font-size: 20px;
    color: #e17055;
    text-align: center;
    margin-bottom: 16px;
}

/* Tips box */
.tips-box {
    background: #fff9f0;
    border: 2px dashed #fdcb6e;
    border-radius: 16px;
    padding: 14px;
    margin-top: 16px;
    font-size: 12px;
    color: #636e72;
    font-weight: 600;
    line-height: 1.8;
}

.tips-box strong {
    color: #e17055;
    font-family: 'Fredoka One', cursive;
    font-size: 14px;
}

/* Footer */
.fun-footer {
    text-align: center;
    padding: 20px;
    margin-top: 32px;
    font-family: 'Fredoka One', cursive;
    font-size: 16px;
    color: #b2bec3;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: #fff9f0 !important;
    border: 2px solid #fab1a0 !important;
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
}

/* Slider */
div[data-testid="stSlider"] > div > div > div {
    background: #e17055 !important;
}

/* Hide streamlit default UI */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 24px !important; }
</style>
""", unsafe_allow_html=True)

# Constants
RESOLUTION_MAP = {
    "Square  1:1  (1024x1024)":   {"ratio": "1:1",  "width": 1024, "height": 1024},
    "Wide  16:9  (1344x768)":     {"ratio": "16:9", "width": 1344, "height": 768},
    "Tall  9:16  (768x1344)":     {"ratio": "9:16", "width": 768,  "height": 1344},
    "Classic  4:3  (1152x896)":   {"ratio": "4:3",  "width": 1152, "height": 896},
}

STYLE_OPTIONS = {
    "No Style":       None,
    "Photo Real":     "photographic",
    "Cinematic":      "cinematic",
    "Digital Art":    "digital-art",
    "Fantasy":        "fantasy-art",
    "Anime":          "anime",
    "Neon Punk":      "neon-punk",
    "3D Model":       "3d-model",
    "Pixel Art":      "pixel-art",
}

STYLE_EMOJIS = {
    "No Style": "✨", "Photo Real": "📷", "Cinematic": "🎬",
    "Digital Art": "🖥️", "Fantasy": "🧙", "Anime": "🌸",
    "Neon Punk": "⚡", "3D Model": "🎲", "Pixel Art": "👾",
}

API_URL   = "https://api.stability.ai/v2beta/stable-image/generate/core"
MAX_RETRY = 3


def call_api(prompt, negative_prompt, ratio, style_key, seed, api_key):
    style_value = STYLE_OPTIONS[style_key]

    payload = {
        "prompt":          prompt,
        "negative_prompt": negative_prompt,
        "aspect_ratio":    ratio,
        "output_format":   "png",
        "seed":            int(seed),
    }
    if style_value:
        payload["style_preset"] = style_value

    headers = {
        "authorization": f"Bearer {api_key}",
        "accept":        "image/*",
    }

    for attempt in range(1, MAX_RETRY + 1):
        try:
            response = requests.post(
                API_URL,
                headers = headers,
                files   = {"none": ""},
                data    = payload,
                timeout = (3.05, 90),
            )

            if response.status_code == 200:
                if response.headers.get("finish-reason") == "FILTER":
                    return None, "Oops! This prompt was blocked. Try a different description."
                return response, None

            if response.status_code in [429, 503]:
                time.sleep((2 ** attempt) + random.uniform(0, 1))
                continue

            if response.status_code == 401:
                return None, "Wrong API key! Please check and try again."

            if response.status_code == 400:
                msg = response.json().get("message", "Something went wrong.")
                return None, f"Request error: {msg}"

            return None, f"Unexpected error: HTTP {response.status_code}"

        except requests.exceptions.ConnectTimeout:
            return None, "Connection timed out. Check your internet!"

        except requests.exceptions.ReadTimeout:
            time.sleep((2 ** attempt) + random.uniform(0, 1))
            continue

    return None, "Too many failed attempts. Please try again later!"


def save_and_verify(response):
    image_bytes = b""
    for chunk in response.iter_content(chunk_size=65536):
        if chunk:
            image_bytes += chunk
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.load()
        return image_bytes, img, None
    except OSError as e:
        return None, None, f"Image was corrupted: {e}"


# ── UI ──────────────────────────────────────────────────

st.markdown("""
<div class="magic-header">
    <div class="stars-row">🌟 ✨ 🌈 ✨ 🌟</div>
    <h1>AI Magic Art Studio</h1>
    <p>Type your idea and watch it come to life!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-mascot">🎨</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Your Art Controls</div>', unsafe_allow_html=True)

    api_key = st.text_input(
        "🔑 API Key",
        type="password",
        placeholder="sk-...",
        help="Get your free key at platform.stability.ai",
    )

    st.markdown("---")

    prompt = st.text_area(
        "💭 What do you want to draw?",
        placeholder="A cute dragon flying over a rainbow castle...",
        height=110,
    )

    negative_prompt = st.text_area(
        "🚫 What to avoid?",
        value="blurry, ugly, watermark, distorted",
        height=70,
    )

    size_choice = st.selectbox(
        "📐 Image Size",
        options=list(RESOLUTION_MAP.keys()),
    )

    style_choice = st.selectbox(
        "🎭 Art Style",
        options=list(STYLE_OPTIONS.keys()),
        format_func=lambda x: f"{STYLE_EMOJIS[x]}  {x}",
    )

    seed = st.slider(
        "🎲 Random Seed",
        min_value=0,
        max_value=9999,
        value=0,
        help="Change this number to get a different result!",
    )

    generate_btn = st.button("✨ Create My Art!")

    st.markdown("""
    <div class="tips-box">
        <strong>Tips for amazing art!</strong><br>
        Add words like:<br>
        "ultra detailed"<br>
        "beautiful lighting"<br>
        "4K quality"<br>
        "professional photo"
    </div>
    """, unsafe_allow_html=True)


# Main output
if generate_btn:
    if not api_key:
        st.error("Please enter your API Key in the sidebar!")
    elif not prompt.strip():
        st.error("Please describe what you want to draw!")
    else:
        dims  = RESOLUTION_MAP[size_choice]

        col1, col2 = st.columns([3, 2])

        with col1:
            with st.spinner("Working on your masterpiece... hang tight!"):
                response, error = call_api(
                    prompt          = prompt.strip(),
                    negative_prompt = negative_prompt.strip(),
                    ratio           = dims["ratio"],
                    style_key       = style_choice,
                    seed            = seed,
                    api_key         = api_key,
                )

            if error:
                st.error(error)
            else:
                with st.spinner("Checking image quality..."):
                    image_bytes, pil_img, verify_error = save_and_verify(response)

                if verify_error:
                    st.error(verify_error)
                else:
                    st.image(image_bytes, use_column_width=True)
                    st.download_button(
                        label     = "💾 Save My Art!",
                        data      = image_bytes,
                        file_name = "my_ai_art.png",
                        mime      = "image/png",
                    )

        with col2:
            if not error and 'pil_img' in dir() and pil_img:
                file_kb = len(image_bytes) / 1024
                style_display = f"{STYLE_EMOJIS[style_choice]} {style_choice}"

                st.markdown(f"""
                <div class="result-card">
                    <h3>Your Art Details</h3>
                    <div class="info-pill">
                        <span class="info-pill-label">Style</span>
                        <span class="info-pill-value">{style_display}</span>
                    </div>
                    <div class="info-pill">
                        <span class="info-pill-label">Size</span>
                        <span class="info-pill-value">{pil_img.width} x {pil_img.height}</span>
                    </div>
                    <div class="info-pill">
                        <span class="info-pill-label">Ratio</span>
                        <span class="info-pill-value">{dims['ratio']}</span>
                    </div>
                    <div class="info-pill">
                        <span class="info-pill-label">File Size</span>
                        <span class="info-pill-value">{file_kb:.1f} KB</span>
                    </div>
                    <div class="info-pill">
                        <span class="info-pill-label">Seed</span>
                        <span class="info-pill-value">{seed}</span>
                    </div>
                    <div class="verified-badge">Image Verified!</div>
                </div>
                """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <span class="big-emoji">🖼️</span>
        <h3>Your artwork will appear here!</h3>
        <p>Fill in the sidebar and hit the magic button</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="fun-footer">
    Made with love by DecodeLabs Batch 2026
</div>
""", unsafe_allow_html=True)
