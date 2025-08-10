import os
import streamlit as st
from utils.db import query
from utils.ui import app_header, nav
from utils.auth import ensure_bootstrap, login_ui, show_first_run_wizard, INITIALIZED_KEY

st.set_page_config(page_title="Loreweave", layout="centered")

# Ensure schema + bootstrap
ensure_bootstrap()

app_header()

with st.sidebar:
    nav()

# --- Version check banner ---
from utils.version import get_latest_info, is_newer, LOCAL_VERSION
latest = get_latest_info()
if latest and is_newer(latest.get("version","0.0.0"), LOCAL_VERSION):
    msg = f"**Update available {latest['version']}** — {latest.get('headline','New release available')}"
    if latest.get("url"):
        msg += f" · [View release]({latest['url']})"
    st.warning(msg)


# First-run wizard if needed
if not st.session_state.get(INITIALIZED_KEY):
    done = show_first_run_wizard()
    if not done:
        st.stop()

# Show home
st.markdown("### Welcome")
name_row = query("SELECT campaign_name FROM app_settings LIMIT 1")
if name_row:
    st.write(f"**Campaign:** {name_row[0]['campaign_name']}")

st.write("This is the **blank** Loreweave starter. Use the Admin Tool to create characters, events, locations and factions.")

# Login / Session
login_ui()

st.info("Tip: Players can browse read-only pages; Admin can edit content in Admin Tool.")
