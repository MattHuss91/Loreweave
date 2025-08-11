import streamlit as st
from utils.db import query, needs_setup
from utils.ui import apply_global_styles, page_title, nav, footer
from utils.auth import ensure_bootstrap, login_ui, show_first_run_wizard, INITIALIZED_KEY
from utils.version import get_latest_info, is_newer, LOCAL_VERSION

st.set_page_config(page_title="Loreweave", layout="centered")
apply_global_styles()

# --- Redirect to Setup if DB isn't ready ---
try:
    if needs_setup():
        st.markdown("## First-time Setup Required")
        st.info("Connect your Postgres database and initialize the schema.")
        # Try to navigate programmatically (Streamlit 1.25+). Fallback to link.
        if st.button("Open Setup Wizard"):
            try:
                st.switch_page("pages/Setup.py")
            except Exception:
                st.write("If you weren't redirected, click: [Setup Wizard](/Setup)")
        st.stop()
except Exception:
    # If needs_setup() itself can't run (e.g., DATABASE_URL missing), send to Setup
    st.markdown("## First-time Setup Required")
    st.info("Connect your Postgres database and initialize the schema.")
    if st.button("Open Setup Wizard"):
        try:
            st.switch_page("pages/Setup.py")
        except Exception:
            st.write("If you weren't redirected, click: [Setup Wizard](/Setup)")
    st.stop()

with st.sidebar:
    nav()

# version notice
latest = get_latest_info()
if latest and is_newer(latest.get("version","0.0.0"), LOCAL_VERSION):
    url = latest.get("url") or "CHANGELOG.md"
    st.warning(f"**Update available {latest['version']}** — {latest.get('headline','New release available')} · [View changes]({url})")

# firsdt run wizard
ensure_bootstrap()
if not st.session_state.get(INITIALIZED_KEY):
    done = show_first_run_wizard()
    if not done:
        st.stop()

page_title("Home")

st.markdown("### Welcome")
name_row = query("SELECT campaign_name FROM app_settings LIMIT 1")
if name_row:
    st.write(f"**Campaign:** {name_row[0]['campaign_name']}")

st.write("Use the Admin Tool to create characters, events, locations and factions.")

login_ui()
footer()
