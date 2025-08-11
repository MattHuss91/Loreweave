import streamlit as st
import pandas as pd
from utils.db import query
from utils.ui import apply_global_styles, page_header, footer

# --- Streamlit config ---
st.set_page_config(page_title="Loreweave • Locations", layout="centered")
apply_global_styles()
page_header("Locations")

# --- Get all locations for dropdown ---
locations = query("""
    SELECT location_id, name, region, description, location_img
    FROM locations
    ORDER BY name
""")
if not locations:
    st.info("No locations yet.")
    footer()
    st.stop()

loc_dict = {loc["name"]: loc["location_id"] for loc in locations}

# --- Location selection ---
selected_name = st.selectbox("Choose a Location", list(loc_dict.keys()))
selected_id = loc_dict[selected_name]

# --- Get selected location details ---
row = query("""
    SELECT location_id, name, region, description, location_img
    FROM locations
    WHERE location_id = %s
""", (selected_id,))

if not row:
    st.warning("Location not found.")
    footer()
    st.stop()

loc = row[0]

# --- Display selected location ---
st.markdown(f"<h2 style='font-family:Cinzel, serif; font-weight:bold; color:black;'>{loc['name']}</h2>", unsafe_allow_html=True)

if loc["region"]:
    st.markdown(f"<p style='font-weight:bold; color:black;'>Region:</p> {loc['region']}", unsafe_allow_html=True)

# Location image - centered & styled
if loc["location_img"]:
    st.markdown(
        f"""
        <div style='display: flex; justify-content: center; margin: 1rem 0;'>
            <img src='{loc['location_img']}' style='max-width: 100%; height: auto; border-radius: 10px;'/>
        </div>
        """,
        unsafe_allow_html=True
    )

# Description
if loc["description"]:
    st.markdown("<h3 style='font-family:Cinzel, serif; font-weight:bold; color:black;'>Description</h3>", unsafe_allow_html=True)
    st.write(loc["description"])
else:
    st.write("No description available.")

footer()
