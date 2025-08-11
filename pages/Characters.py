import streamlit as st
import os
from utils.db import query, execute
from utils.auth import login_ui
from utils.time import parse_date

from utils.ui import apply_global_styles, page_header, card, footer

st.set_page_config(page_title="Loreweave • <PageName>", layout="centered")
apply_global_styles()
page_header("<PageName>")

qid = st.query_params.get("character_id", [None])[0]

rows = query("SELECT character_id,name,type,status,bio,character_img,is_player FROM characters ORDER BY name")
if not rows:
    st.info("No characters yet.")
else:
    for r in rows:
        label = f"{r['name']} — {r['type'] or 'Unknown'}"
        default_open = (qid is not None and str(r['character_id']) == str(qid))
        with st.expander(label, expanded=default_open):
            if r['character_img']:
                st.image(r['character_img'])
            st.write(f"**Status:** {r['status'] or 'Unknown'}")
            st.write(r['bio'] or "")
            evs = query("""
                SELECT e.event_id, e.title, e.date_occurred
                FROM characterappearances ca
                JOIN campaignevents e ON e.event_id = ca.event_id
                WHERE ca.character_id = %s
                ORDER BY e.world_day
            """, (r['character_id'],))
            if evs:
                st.markdown("**Appears in:** " + ", ".join(
                    [f"[{e['title']}](/pages/Events?event_id={e['event_id']})" for e in evs]
                ))

footer()
