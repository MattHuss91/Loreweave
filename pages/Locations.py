import os
import streamlit as st
from utils.db import query, execute
from utils.auth import login_ui
from utils.time import parse_date

from utils.ui import apply_global_styles, page_header, card, footer

st.set_page_config(page_title="Loreweave • <PageName>", layout="centered")
apply_global_styles()
page_header("<PageName>")

st.set_page_config(page_title="Admin Tool", layout="centered")


rows = query("SELECT location_id,name,description,location_img FROM locations ORDER BY name")
if not rows:
    st.info("No locations yet.")
else:
    for r in rows:
        with st.expander(r['name']):
            if r['location_img']:
                st.image(r['location_img'])
            st.write(r['description'] or "")

footer()
