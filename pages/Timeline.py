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


# --- Helpers ---
def _ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n % 10]}"

def format_world_date(world_day: int) -> str:
    months = [
        "Verdanir", "Emberfall", "Duskwatch", "Glimmerwane", "Brightreach",
        "Stormrest", "Hollowshade", "Deepmoor", "Frostmere", "Starwake"
    ]
    days_per_month = 36
    days_per_year = days_per_month * len(months)

    year = (world_day // days_per_year) + 1
    day_of_year = world_day % days_per_year
    month_index = day_of_year // days_per_month
    day_in_month = (day_of_year % days_per_month) + 1

    return f"{_ordinal(day_in_month)} {months[month_index]} {year}ASF"

bounds = query("SELECT COALESCE(MIN(world_day),0) AS min_wd, COALESCE(MAX(world_day),360) AS max_wd FROM campaignevents")
wd_min, wd_max = bounds[0]["min_wd"], bounds[0]["max_wd"]
if wd_min == wd_max:
    wd_min = 0

# Show human-readable labels for min/max
st.write(f"**Date range:** {format_world_date(int(wd_min))} → {format_world_date(int(wd_max or 360))}")

wd_range = st.slider(
    "World day range",
    min_value=int(wd_min),
    max_value=int(wd_max or 360),
    value=(int(wd_min), int(wd_max or 360))
)

# Echo the selection in human-readable form
st.write(f"Selected: {format_world_date(wd_range[0])} → {format_world_date(wd_range[1])}")

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
        header = f"{format_world_date(int(r['world_day']))} — {r['title']} ({r['date_occurred'] or 'Unknown'})"
        with st.expander(header):
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

