import streamlit as st

# ---- GLOBAL STYLE KIT ----
def apply_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    /* App background / global font */
    .stApp {
        background-image: url('https://i.imgur.com/v0Jdhpp.jpeg');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        font-family: 'Lora', serif !important;
        color: #000000 !important;
    }

    /* Main container */
    .block-container {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 1.0rem 1.0rem 1.25rem 1.0rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }

    /* Headings */
    h1, h2, h3, .app-title {
        font-family: 'Cinzel', serif !important;
        color: #222;
        letter-spacing: 0.5px;
    }
    h1 { text-transform: uppercase; }
    h2, h3 { text-transform: none; }

    /* Labels / inputs / buttons */
    label { color:#000 !important; font-weight:600; }
    div.stButton > button, .stDownloadButton button {
        background-color:#333 !important; color:#fff !important;
        font-weight:700 !important; font-family:'Cinzel', serif !important;
        border:none !important; border-radius:10px !important;
        padding: .6rem 1.0rem !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        background: #1f232a; color:#fff; border-radius:10px; border:1px solid #2e3440;
    }

    /* Cards / helpers */
    .lw-card {
        background: rgba(255,255,255,0.85);
        padding: .85rem 1rem; border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,.06);
        margin: .5rem 0 1rem 0;
    }
    .lw-hr { border:none; border-top:1px solid rgba(0,0,0,.15); margin: 1rem 0; }

    /* Centered brand header */
    .lw-brand { text-align:center; margin-top:-14px; margin-bottom:.25rem; }
    .lw-brand img { width:200px; margin-bottom:-6px; }
    </style>
    """, unsafe_allow_html=True)

def page_header(title: str, subtitle: str | None = None, logo_url: str = "https://i.imgur.com/WEGvkz8.png"):
    st.markdown(f"""
    <div class="lw-brand">
      <img src="{logo_url}" />
      <h1 class="app-title" style="margin-top:0;">{title.upper()}</h1>
      {f"<div style='opacity:.85;'>{subtitle}</div>" if subtitle else ""}
    </div>
    <div class="lw-hr"></div>
    """, unsafe_allow_html=True)

def card(md: str):
    st.markdown(f"<div class='lw-card'>{md}</div>", unsafe_allow_html=True)

def footer():
    st.markdown("<div class='lw-hr'></div>", unsafe_allow_html=True)
    st.caption("Powered by Loreweave • © 2025 Matthew Husselbury")
