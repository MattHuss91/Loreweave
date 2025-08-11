import streamlit as st

# ---- GLOBAL STYLE KIT ----
def apply_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');

    /* Background + base font */
    .stApp {
        background-image: url('https://i.imgur.com/v0Jdhpp.jpeg');
        background-size: cover; background-attachment: fixed;
        background-repeat: no-repeat; background-position: center;
        font-family: 'Lora', serif !important;
        color: #000000 !important; /* body text black (like personal) */
    }

    /* Remove white container */
    .main .block-container { background: transparent !important; box-shadow:none !important; padding-top: 1rem !important; }

    /* Headings */
    h1, h2, h3 { font-family:'Cinzel', serif !important; color:#000000 !important; text-transform: uppercase; }

    /* Event titles – match personal spacing/size */
    h2 {
      font-size: 2.2rem !important;
      letter-spacing: .5px !important;
      margin: 1.4rem 0 .6rem 0 !important;
    }

    /* Labels */
    .stSelectbox label, .stSlider label, label { color:#000000 !important; font-weight:700 !important; }

    /* Selectbox: dark, white text (personal look) */
    .stSelectbox div[data-baseweb="select"] > div {
        background:#2c2f35 !important;
        color:#ffffff !important;
        border-radius:10px !important;
        border:1px solid rgba(0,0,0,.3) !important;
        min-height:48px !important;
        padding-left:.5rem !important;
    }

    /* Text inputs (keep dark like personal) */
    .stTextInput input, .stTextArea textarea {
        background:#2c2f35 !important;
        color:#ffffff !important;
        border-radius:10px !important;
        border:1px solid rgba(0,0,0,.3) !important;
    }

    /* Slider (BaseWeb) – dark rail, red accent, readable tick labels */
    .stSlider [data-baseweb="slider"] > div { background:transparent !important; }
    .stSlider [data-baseweb="slider"] div[role="slider"] { box-shadow:none !important; }
    .stSlider [data-baseweb="slider"] div[role="slider"]::before { display:none !important; }
    .stSlider [data-baseweb="slider"] > div > div { background:rgba(44,47,53,.4) !important; }  /* rail */
    .stSlider [data-baseweb="slider"] > div > div > div { background:#ef6b6b !important; }      /* track (red like personal) */
    .stSlider [data-baseweb="slider"] div[role="slider"] { background:#ef6b6b !important; }     /* handle */
    .stSlider label + div span { color:#000000 !important; font-weight:600 !important; }        /* edge labels */

    /* Hide the select_slider's grey value badges under the rail */
    .stSlider [data-baseweb="slider"] > div > div + div { display: none !important; }

    /* Expander – subtle card look */
    details.st-expander > summary {
        background: rgba(255,255,255,0.85) !important;
        border-radius: 10px !important;
        padding: .65rem 1rem !important;
        border: 1px solid rgba(0,0,0,.08) !important;
        font-weight:700 !important;
    }
    details.st-expander > div[aria-expanded="true"] {
        background: rgba(255,255,255,0.85) !important;
        border-radius: 0 0 10px 10px !important;
        border-left: 1px solid rgba(0,0,0,.08) !important;
        border-right: 1px solid rgba(0,0,0,.08) !important;
        border-bottom: 1px solid rgba(0,0,0,.08) !important;
        padding: .5rem 1rem 1rem 1rem !important;
    }

    /* Buttons */
    div.stButton > button {
        background:#333 !important; color:#fff !important;
        font-weight:700 !important; font-family:'Cinzel', serif !important;
        border:none !important; border-radius:10px !important; padding:.6rem 1rem !important;
    }

    /* Brand header + divider */
    .lw-brand { text-align:center; margin-top:-14px; margin-bottom:.25rem; }
    .lw-brand img { width:200px; margin-bottom:-6px; }
    .lw-hr { border:none; border-top:1px solid rgba(0,0,0,.15); margin: 1rem 0; }
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
