import os
import streamlit as st
import pandas as pd
import urllib.parse
from utils.db import query
from utils.ui import apply_global_styles, page_header, footer

st.set_page_config(page_title="Loreweave • Timeline", layout="centered")
apply_global_styles()
page_header("Timeline")

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

# --- Read query params for deep-linking ---
query_params = st.query_params
highlight_event = query_params.get("highlight", [""])[0]
from_character_id = query_params.get("from_character_id", [""])[0]

# --- Pull events from DB ---
rows = query("""
    SELECT e.event_id, e.title, e.date_occurred, e.summary, e.full_description,
           e.world_day, l.name AS location,
           STRING_AGG(c.name, ', ') AS people_involved
    FROM campaignevents e
    LEFT JOIN locations l ON l.location_id = e.location_id
    LEFT JOIN characterappearances ca ON e.event_id = ca.event_id
    LEFT JOIN characters c ON c.character_id = ca.character_id
    GROUP BY e.event_id, l.name
    ORDER BY e.world_day
""")

if not rows:
    st.info("No events found in the database.")
    footer()
    st.stop()

df = pd.DataFrame(rows)

# --- Highlighted event filter ---
if highlight_event:
    df = df[df["title"].str.strip().str.lower() == highlight_event.strip().lower()]
    if df.empty:
        st.warning(f"No event found matching: '{highlight_event}'")

# --- Back to character link ---
if from_character_id.isdigit():
    char_name_row = query("SELECT name FROM characters WHERE character_id = %s", (from_character_id,))
    if char_name_row:
        char_name = char_name_row[0]['name']
        st.markdown(f"[← Back to {char_name}](/pages/Characters?character_id={from_character_id})")

# --- Filters ---
if not highlight_event:
    # Character filter
    all_chars = sorted(set(
        name.strip() for sub in df['people_involved'].dropna().str.split(',') for name in sub
    ))
    selected_character = st.selectbox("Filter by character", ["All"] + all_chars)
    if selected_character != "All":
        df = df[df['people_involved'].str.contains(selected_character)]

    # Date slider
    if not df.empty:
        wd_unique = sorted(df['world_day'].dropna().unique())
        wd_labels = {wd: format_world_date(wd) for wd in wd_unique}
        start_wd, end_wd = st.select_slider(
            "Select a date range",
            options=wd_unique,
            format_func=lambda x: wd_labels[x],
            value=(wd_unique[0], wd_unique[-1])
        )
        df = df[(df['world_day'] >= start_wd) & (df['world_day'] <= end_wd)]
    else:
        st.warning("No events match your selected filters.")
        footer()
        st.stop()

# --- Render timeline ---
for _, row in df.iterrows():
    header = f"{format_world_date(int(row['world_day']))} — {row['title']} ({row['date_occurred'] or 'Unknown'})"
    with st.expander(header):
        st.write(f"**Location:** {row['location'] or 'Unspecified'}")
        st.markdown(f"**Summary:** {row['summary'] or 'No summary'}")
        if row['full_description']:
            st.write(row['full_description'])
        if row['people_involved']:
            st.markdown("**People Involved:**")
            for character in row['people_involved'].split(', '):
                char_id = query("SELECT character_id FROM characters WHERE name = %s", (character,))
                if char_id:
                    st.markdown(f"- [{character}](/pages/Characters?character_id={char_id[0]['character_id']})")

footer()
