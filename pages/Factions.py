import streamlit as st
from utils.db import query
from utils.ui import apply_global_styles, page_header, footer

# --- Streamlit config ---
st.set_page_config(page_title="Loreweave • Factions", layout="centered")
apply_global_styles()
page_header("Factions")

# --- Get all factions for dropdown ---
factions = query("""
    SELECT faction_id, name, alignment, goals, faction_img
    FROM factions
    ORDER BY name
""")
if not factions:
    st.info("No factions yet.")
    footer()
    st.stop()

fac_dict = {f["name"]: f["faction_id"] for f in factions}

# --- Faction selection ---
selected_name = st.selectbox("Choose a Faction", list(fac_dict.keys()))
selected_id = fac_dict[selected_name]

# --- Get selected faction details ---
row = query("""
    SELECT faction_id, name, alignment, goals, faction_img
    FROM factions
    WHERE faction_id = %s
""", (selected_id,))

if not row:
    st.warning("Faction not found.")
    footer()
    st.stop()

fac = row[0]

# --- Display faction details (match Locations styling) ---
st.markdown(
    f"""
    <h2 style="
        font-family: Cinzel, serif;
        font-weight: 700;
        color: #000;
        text-transform: uppercase;
        text-align: center;
        letter-spacing: .5px;
        margin: 1.2rem 0 .4rem 0;
    ">{fac['name']}</h2>
    """,
    unsafe_allow_html=True
)

if fac["alignment"]:
    st.markdown(
        f"""
        <h3 style="font-family:Cinzel,serif; color:#000; margin:.6rem 0;">
            <span style="font-weight:700;">Alignment:</span>
            <span style="font-weight:400;"> {fac['alignment']}</span>
        </h3>
        """,
        unsafe_allow_html=True
    )

# Faction image - centered
if fac["faction_img"]:
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin: 1rem 0;">
            <img src="{fac['faction_img']}" style="max-width:100%; height:auto; border-radius:10px;" />
        </div>
        """,
        unsafe_allow_html=True
    )

# Goals / description
if fac["goals"]:
    st.markdown(
        '<h3 style="font-family:Cinzel,serif; font-weight:700; color:#000; margin-top:1rem;">Goals</h3>',
        unsafe_allow_html=True
    )
    st.write(fac["goals"])
else:
    st.write("No goals available.")

# --- Members ---
members = query("""
    SELECT c.character_id, c.name
    FROM characterfactions cf
    JOIN characters c ON c.character_id = cf.character_id
    WHERE cf.faction_id = %s
    ORDER BY c.name
""", (selected_id,))

if members:
    st.markdown(
        '<h3 style="font-family:Cinzel,serif; font-weight:700; color:#000; margin-top:1rem;">Members</h3>',
        unsafe_allow_html=True
    )
    for m in members:
        st.markdown(f"- [{m['name']}](/pages/Characters?character_id={m['character_id']})")
else:
    st.write("No members listed.")

footer()
