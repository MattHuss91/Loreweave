import streamlit as st
from utils.ui import apply_global_styles, page_title, nav, footer
from utils.db import query

st.set_page_config(page_title="Events", layout="centered")
apply_global_styles()
with st.sidebar:
    nav()
page_title("Events")

eid = st.query_params.get("event_id", [None])[0]

rows = query("""
SELECT e.event_id,e.title,e.date_occurred,e.summary,l.name AS location,e.world_day
FROM campaignevents e LEFT JOIN locations l ON e.location_id=l.location_id
ORDER BY e.world_day
""")
if not rows:
    st.info("No events yet.")
else:
    for r in rows:
        label = f"{r['title']} — {r['date_occurred'] or 'Unknown'}"
        default_open = (eid is not None and str(r['event_id']) == str(eid))
        with st.expander(label, expanded=default_open):
            st.write(f"**Location:** {r['location'] or 'Unspecified'}")
            st.write(r['summary'] or "")
            chars = query("""
                SELECT c.character_id, c.name FROM characterappearances ca
                JOIN characters c ON c.character_id = ca.character_id
                WHERE ca.event_id = %s ORDER BY c.name
            """, (r["event_id"],))
            if chars:
                st.markdown("**Characters:** " + ", ".join(
                    [f"[{c['name']}](/pages/Characters?character_id={c['character_id']})" for c in chars]
                ))

footer()
