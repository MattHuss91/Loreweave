import streamlit as st
from utils.ui import app_header, nav
from utils.db import query

st.set_page_config(page_title="Events", layout="centered")
app_header()

with st.sidebar:
    nav()

st.subheader("Events")

rows = query("""SELECT e.event_id,e.title,e.date_occurred,e.summary,l.name AS location
                   FROM campaignevents e LEFT JOIN locations l ON e.location_id=l.location_id
                   ORDER BY e.world_day""")
if not rows:
    st.info("No events yet.")
else:
    for r in rows:
        with st.expander(f"{r['title']} — {r['date_occurred'] or 'Unknown'}"):
            st.write(f"**Location:** {r['location'] or 'Unspecified'}")
            st.write(r['summary'] or "")

