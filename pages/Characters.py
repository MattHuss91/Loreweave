import streamlit as st
from utils.ui import app_header, nav
from utils.db import query

st.set_page_config(page_title="Characters", layout="centered")
app_header()

with st.sidebar:
    nav()

st.subheader("Characters")

rows = query("SELECT character_id,name,type,status,bio,character_img,is_player FROM characters ORDER BY name")
if not rows:
    st.info("No characters yet.")
else:
    for r in rows:
        with st.expander(f"{r['name']} — {r['type']}"):
            if r['character_img']:
                st.image(r['character_img'])
            st.write(f"**Status:** {r['status']}")
            st.write(r['bio'] or "")
            st.caption("Player character" if r['is_player'] else "NPC")

