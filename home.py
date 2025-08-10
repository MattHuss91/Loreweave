import streamlit as st
from utils.db import query
from utils.ui import apply_global_styles, page_title, nav, footer
from utils.auth import ensure_bootstrap, login_ui, show_first_run_wizard, INITIALIZED_KEY
from utils.version import get_latest_info, is_newer, LOCAL_VERSION

st.set_page_config(page_title="Loreweave", layout="centered")

ensure_bootstrap()
apply_global_styles()

with st.sidebar:
    nav()

latest = get_latest_info()
if latest and is_newer(latest.get("version","0.0.0"), LOCAL_VERSION):
    url = latest.get("url") or "CHANGELOG.md"
    st.warning(f"**Update available {latest['version']}** — {latest.get('headline','New release available')} · [View changes]({url})")

if not st.session_state.get(INITIALIZED_KEY):
    done = show_first_run_wizard()
    if not done:
        st.stop()

page_title("Home")

st.markdown("### Welcome")
name_row = query("SELECT campaign_name FROM app_settings LIMIT 1")
if name_row:
    st.write(f"**Campaign:** {name_row[0]['campaign_name']}")

st.write("This is the **Loreweave Blank** starter. Use the Admin Tool to create characters, events, locations and factions.")

login_ui()
footer()
