import streamlit as st
from utils.ui import apply_global_styles, page_title, nav, footer
from utils.db import query

st.set_page_config(page_title="Timeline", layout="centered")
apply_global_styles()
with st.sidebar:
    nav()
page_title("Timeline")

bounds = query("SELECT COALESCE(MIN(world_day),0) AS min_wd, COALESCE(MAX(world_day),360) AS max_wd FROM campaignevents")
wd_min, wd_max = bounds[0]["min_wd"], bounds[0]["max_wd"]
if wd_min == wd_max:
    wd_min = 0
wd_range = st.slider("World day range", min_value=int(wd_min), max_value=int(wd_max or 360), value=(int(wd_min), int(wd_max or 360)))

locs = query("SELECT location_id, name FROM locations ORDER BY name")
loc_names = ["(Any)"] + [r["name"] for r in locs]
loc_filter = st.selectbox("Location filter", loc_names)

rows = query("""
SELECT e.event_id, e.title, e.date_occurred, e.world_day, l.name AS location
FROM campaignevents e LEFT JOIN locations l ON l.location_id = e.location_id
WHERE (e.world_day BETWEEN %s AND %s)
  AND (%s = '(Any)' OR l.name = %s)
ORDER BY e.world_day
""", (wd_range[0], wd_range[1], loc_filter, loc_filter))

if not rows:
    st.info("No events in this range yet.")
else:
    for r in rows:
        with st.expander(f"{r['world_day']:>4} — {r['title']} ({r['date_occurred'] or 'Unknown'})"):
            st.write(f"**Location:** {r['location'] or 'Unspecified'}")
            chars = query("""
                SELECT c.character_id, c.name, c.type
                FROM characterappearances ca JOIN characters c ON c.character_id = ca.character_id
                WHERE ca.event_id = %s ORDER BY c.name
            """, (r['event_id'],))
            if chars:
                st.markdown("**Characters:** " + ", ".join(
                    [f"[{c['name']}](/pages/Characters?character_id={c['character_id']})" for c in chars]
                ))

footer()
