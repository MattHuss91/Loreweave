import os
import streamlit as st

def app_header():
    st.markdown("""
    <div style='text-align: center; margin-top: -10px;'>
        <img src='https://i.imgur.com/WEGvkz8.png' style='width: 180px; margin-bottom: -6px;' />
        <h1 style='margin-top: 0; font-family: "Cinzel", serif;'>Loreweave</h1>
    </div>
    """, unsafe_allow_html=True)

def nav():
    st.page_link("home.py", label="Home", icon="🏠")
    st.page_link("pages/Characters.py", label="Characters", icon="🧙")
    st.page_link("pages/Events.py", label="Events", icon="📜")
    st.page_link("pages/Locations.py", label="Locations", icon="🗺️")
    st.page_link("pages/Factions.py", label="Factions", icon="🛡️")
    st.page_link("pages/Admin Tool.py", label="Admin Tool", icon="🛠️")
