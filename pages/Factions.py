import streamlit as st
from utils.ui import apply_global_styles, page_title, nav, footer
from utils.db import query

st.set_page_config(page_title="Factions", layout="centered")
apply_global_styles()
with st.sidebar:
    nav()
page_title("Factions")

rows = query("SELECT faction_id,name,alignment,goals,faction_img FROM factions ORDER BY name")
if not rows:
    st.info("No factions yet.")
else:
    for r in rows:
        with st.expander(f"{r['name']} — {r['alignment'] or 'Neutral'}"):
            if r['faction_img']:
                st.image(r['faction_img'])
            st.write(r['goals'] or "")
            members = query("""
                SELECT c.character_id, c.name
                FROM characterfactions cf JOIN characters c ON c.character_id = cf.character_id
                WHERE cf.faction_id = %s ORDER BY c.name
            """, (r['faction_id'],))
            if members:
                st.markdown("**Members:** " + ", ".join(
                    [f"[{m['name']}](/pages/Characters?character_id={m['character_id']})" for m in members]
                ))

footer()
