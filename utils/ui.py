import streamlit as st

LOREWEAVE_LOGO = "https://i.imgur.com/WEGvkz8.png"
PARCHMENT_BG = "https://i.imgur.com/v0Jdhpp.jpeg"

def apply_global_styles():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');
    .stApp {{
        background-image: url('{PARCHMENT_BG}');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        font-family: 'Lora', serif !important;
        color: #000000 !important;
    }}
    label {{
        color: #000000 !important;
        font-weight: bold;
    }}
    div.stButton > button {{
        background-color: #333333 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-family: 'Cinzel', serif !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 5px !important;
    }}
    .lw-footer {{
        text-align:center; font-size: 12px; margin-top: 2rem; opacity: 0.85;
    }}
    </style>
    """, unsafe_allow_html=True)

def page_title(title_text: str):
    st.markdown(f"""
        <div style='text-align: center; margin-top: -20px;'>
            <img src='{LOREWEAVE_LOGO}' style='width: 200px; margin-bottom: -10px;' />
            <h1 style='margin-top: 0; font-family: "Cinzel", serif; text-transform: uppercase;'>{title_text}</h1>
        </div>
    """, unsafe_allow_html=True)

def nav():
    st.page_link("home.py", label="HOME", icon="🏠")
    st.page_link("pages/Timeline.py", label="TIMELINE", icon="🗓️")
    st.page_link("pages/Characters.py", label="CHARACTERS", icon="🧙")
    st.page_link("pages/Events.py", label="EVENTS", icon="📜")
    st.page_link("pages/Locations.py", label="LOCATIONS", icon="🗺️")
    st.page_link("pages/Factions.py", label="FACTIONS", icon="🛡️")
    st.page_link("pages/Admin Tool.py", label="ADMIN TOOL", icon="🛠️")

def footer():
    st.markdown("<div class='lw-footer'>Powered by Loreweave • © 2025 Matthew Husselbury</div>", unsafe_allow_html=True)
