import streamlit as st
from utils.ui import apply_global_styles, page_title, nav, footer
from utils.db import query

st.set_page_config(page_title="Characters", layout="centered")
apply_global_styles()
with st.sidebar:
    nav()
page_title("Characters")

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
