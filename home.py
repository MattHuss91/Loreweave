# pages/Home.py
import streamlit as st
from utils.db import query, needs_setup
from utils.ui import apply_global_styles, page_title, nav, footer
from utils.auth import ensure_bootstrap, login_ui, show_first_run_wizard, INITIALIZED_KEY
from utils.version import get_latest_info, is_newer, LOCAL_VERSION
from datetime import date

st.set_page_config(page_title="Loreweave", layout="centered")
apply_global_styles()

# --- Hardening: redirect to Setup if DB isn't ready ---
try:
    if needs_setup():
        st.markdown("""
            <div style='text-align: center; margin-top: -10px;'>
                <img src='https://i.imgur.com/WEGvkz8.png' style='width: 180px; margin-bottom: -6px;' />
                <h1 style='margin-top: 0; font-family: "Cinzel", serif;'>First-time Setup Required</h1>
            </div>
        """, unsafe_allow_html=True)
        st.info("Connect your Postgres database and initialize the schema.")
        if st.button("Open Setup Wizard"):
            try:
                st.switch_page("pages/Setup.py")
            except Exception:
                st.write("If you weren't redirected, click: [Setup Wizard](/Setup)")
        st.stop()
except Exception:
    st.markdown("""
        <div style='text-align: center; margin-top: -10px;'>
            <img src='https://i.imgur.com/WEGvkz8.png' style='width: 180px; margin-bottom: -6px;' />
            <h1 style='margin-top: 0; font-family: "Cinzel", serif;'>First-time Setup Required</h1>
        </div>
    """, unsafe_allow_html=True)
    st.info("Connect your Postgres database and initialize the schema.")
    if st.button("Open Setup Wizard"):
        try:
            st.switch_page("pages/Setup.py")
        except Exception:
            st.write("If you weren't redirected, click: [Setup Wizard](/Setup)")
    st.stop()

with st.sidebar:
    nav()

# --- Extra visual styling to match your personal build ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');
.stApp { 
    background-image: url('https://i.imgur.com/v0Jdhpp.jpeg'); 
    background-size: cover; background-attachment: fixed; background-repeat: no-repeat; background-position: center;
    font-family: 'Lora', serif !important;
}
.block-container { color: #000000; }
h1, h2, h3 { font-family: 'Cinzel', serif !important; text-transform: none; }
label { color:#000000 !important; font-weight:bold; }
div.stButton > button {
    background-color:#333333 !important; color:#ffffff !important; font-weight:bold !important; 
    font-family:'Cinzel', serif !important; border:none !important; padding:0.5rem 1rem !important; border-radius:5px !important;
}
.date-card {
    background: rgba(255,255,255,0.85);
    padding: .75rem 1rem; border-radius: 10px; text-align: center; margin: .75rem 0 1rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,.08);
}
.hr-soft { border:none; border-top:1px solid rgba(0,0,0,.15); margin: 1rem 0; }
.brand-wrap { text-align:center; margin-top: -20px; }
.brand-wrap img { width:200px; margin-bottom:-10px; }
</style>
""", unsafe_allow_html=True)

# --- Brand header (logo + title/campaign) ---
st.markdown("""
<div class="brand-wrap">
  <img src="https://i.imgur.com/WEGvkz8.png" />
  <h1 style='margin-top: 0;'>Loreweave</h1>
</div>
""", unsafe_allow_html=True)

# --- Version notice (unchanged logic) ---
latest = get_latest_info()
if latest and is_newer(latest.get("version", "0.0.0"), LOCAL_VERSION):
    url = latest.get("url") or "CHANGELOG.md"
    st.warning(f"**Update available {latest['version']}** — {latest.get('headline','New release available')} · [View changes]({url})")

# --- Bootstrap any required rows and run first-run wizard once ---
ensure_bootstrap()
if not st.session_state.get(INITIALIZED_KEY):
    done = show_first_run_wizard()
    if not done:
        st.stop()

# --- Fantasy calendar display (matches your personal widget)  :contentReference[oaicite:2]{index=2}
def get_ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return f"{n}{suffix}"

def fantasy_today():
    months = ["Verdanir","Emberfall","Duskwatch","Glimmerwane","Brightreach","Stormrest","Hollowshade","Deepmoor","Frostmere","Starwake"]
    weekdays = ["Sunsday","Moonday","Wyrmday","Gloomday","Thornsday","Brightsday"]
    days_per_month, days_per_year = 36, 360

    anchor = date(2025, 1, 1)
    today = date.today()
    delta = (today - anchor).days
    world_day = delta % days_per_year

    month_idx = world_day // days_per_month
    day_of_month = (world_day % days_per_month) + 1
    weekday = weekdays[delta % 6]
    return weekday, day_of_month, months[month_idx], today.strftime("%A %d %B")

wd, d, mo, irl = fantasy_today()
st.markdown(f"""
<div class="date-card">
  <strong>Today in the world</strong><br/>
  <em>{wd}, {get_ordinal(d)} of {mo}</em><br/>
  <small>(IRL: {irl})</small>
</div>
""", unsafe_allow_html=True)

# --- Page title + Campaign name from DB ---
page_title("Home")
row = query("SELECT campaign_name FROM app_settings LIMIT 1")
if row:
    st.markdown(f"### Campaign: **{row[0]['campaign_name']}**")

st.write("Use the Admin Tool to create characters, events, locations, and factions.")

# --- Auth UI (your central login component) ---
login_ui()

st.markdown('<div class="hr-soft"></div>', unsafe_allow_html=True)
footer()
