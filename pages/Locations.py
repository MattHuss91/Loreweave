import streamlit as st
from utils.ui import app_header, nav
from utils.db import query

st.set_page_config(page_title="Locations", layout="centered")
app_header()

with st.sidebar:
    nav()

st.subheader("Locations")

rows = query("SELECT location_id,name,description,location_img FROM locations ORDER BY name")
if not rows:
    st.info("No locations yet.")
else:
    for r in rows:
        with st.expander(r['name']):
            if r['location_img']:
                st.image(r['location_img'])
            st.write(r['description'] or "")

