import streamlit as st

# ---- GLOBAL STYLE KIT ----
def apply_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    /* App background & font */
    .stApp {
        background-image: url('https://i.imgur.com/v0Jdhpp.jpeg');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        font-family: 'Lora', serif !important;
        color: #000000 !important;
    }

    /* Remove white content background for all pages */
    .main .block-container {
        background-color: transparent !important;
        box-shadow: none !important;
        padding-top: 1rem !important;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: #000000 !important;
        text-transform: uppercase;
    }

   /* Form labels for selectbox, slider, etc. */
.stSelectbox label, .stSlider label, label {
    color: #000000 !important;  /* Changed from white to black */
    font-weight: bold !important;
}

   /* Widget backgrounds */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.6) !important; /* lighter background for black text */
    color: #000000 !important;
    border-radius: 8px !important;
    }
.stTextInput input, .stTextArea textarea {
    background-color: rgba(255,255,255,0.6) !important;
    color: #000000 !important;
    border-radius: 8px !important;
    }


    /* Buttons */
    div.stButton > button {
        background-color: #333333 !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-family: 'Cinzel', serif !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
    }

    /* Cards (if used via card() helper) */
    .lw-card {
        background: rgba(255,255,255,0.1);
        padding: .85rem 1rem;
        border-radius: 12px;
        margin: .5rem 0 1rem 0;
    }

    .lw-hr {
        border:none;
        border-top:1px solid rgba(255,255,255,.3);
        margin: 1rem 0;
    }

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
