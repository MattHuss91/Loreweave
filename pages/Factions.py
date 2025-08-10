import streamlit as st
from utils.ui import app_header, nav
from utils.db import query

st.set_page_config(page_title="Factions", layout="centered")
app_header()

with st.sidebar:
    nav()

st.subheader("Factions")

rows = query("SELECT faction_id,name,alignment,goals,faction_img FROM factions ORDER BY name")
if not rows:
    st.info("No factions yet.")
else:
    for r in rows:
        with st.expander(f"{r['name']} — {r['alignment'] or 'Neutral'}"):
            if r['faction_img']:
                st.image(r['faction_img'])
            st.write(r['goals'] or "")

