import os
import streamlit as st
import bcrypt
from .db import query, execute, run_sql_file

SCHEMA_OK_KEY = "schema_ok"
INITIALIZED_KEY = "initialized"
CAL_SETUP_DONE = "calendar_setup_done"

def ensure_bootstrap():
    try:
        _ = query("SELECT 1 FROM information_schema.tables WHERE table_name='app_settings'")
    except Exception:
        st.error("Cannot connect to the database. Make sure DATABASE_URL is set and reachable.")
        st.stop()

    app_settings_tbl = query("SELECT table_name FROM information_schema.tables WHERE table_name='app_settings'")
    if not app_settings_tbl:
        base = os.path.dirname(os.path.dirname(__file__))
        run_sql_file(os.path.join(base, "sql", "init_db.sql"))
        run_sql_file(os.path.join(base, "sql", "seed_calendar.sql"))
        st.success("Database initialized.")

    st.session_state[SCHEMA_OK_KEY] = True

    rows = query("SELECT * FROM app_settings LIMIT 1")
    if not rows:
        campaign_name = os.getenv("CAMPAIGN_NAME", None)
        if campaign_name:
            execute("INSERT INTO app_settings (campaign_name) VALUES (%s)", (campaign_name,))

    admins = query("SELECT 1 FROM users WHERE is_admin=true LIMIT 1")
    st.session_state[INITIALIZED_KEY] = bool(query("SELECT 1 FROM app_settings LIMIT 1")) and bool(admins)

def show_first_run_wizard():
    st.header("First-run Setup")
    st.write("Name your campaign, create the Admin account, and (optionally) customize your calendar.")

    with st.form("first_run_main"):
        cname = st.text_input("Campaign name", placeholder="Your Campaign")
        user = st.text_input("Admin username", value="Admin")
        pwd = st.text_input("Admin password", type="password")
        cal_toggle = st.checkbox("Customize calendar (optional)", value=False)
        cal_text = st.text_area(
            "Months (name days per line, e.g. 'Verdanir 36')",
            value="Verdanir 36\nEmberfall 36\nDuskwatch 36\nGlimmerwane 36\nBrightreach 36\nStormrest 36\nHollowshade 36\nDeepmoor 36\nFrostmere 36\nStarwake 36",
            disabled=not cal_toggle,
            height=180
        )
        ok = st.form_submit_button("Initialize")

    if ok:
        if not cname or not user or not pwd:
            st.error("Please fill campaign name and admin credentials.")
            return False
        execute("INSERT INTO app_settings (campaign_name) VALUES (%s)", (cname,))
        pw_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        execute("INSERT INTO users (username,password_hash,is_admin) VALUES (%s,%s,true)", (user, pw_hash))

        if cal_toggle:
            execute("DELETE FROM calendar_months", ())
            execute("DELETE FROM calendar_settings", ())
            lines = [ln.strip() for ln in cal_text.splitlines() if ln.strip()]
            months = []
            for i, ln in enumerate(lines, start=1):
                parts = ln.split()
                name = " ".join(parts[:-1])
                days = int(parts[-1])
                months.append((i, name, days))
            total = len(months) if months else 10
            default_days = months[0][2] if months else 36
            execute("INSERT INTO calendar_settings (total_months, default_days_per_month) VALUES (%s,%s)", (total, default_days))
            for (mid, name, days) in months:
                execute("INSERT INTO calendar_months (month_id,name,days) VALUES (%s,%s,%s)", (mid, name, days))
        st.success("Initialized! You can now log in as Admin.")
        st.session_state[INITIALIZED_KEY] = True
        st.session_state[CAL_SETUP_DONE] = True
        return True
    return False

def login_ui():
    st.session_state.setdefault("username", "")
    st.session_state.setdefault("is_admin", False)

    if st.session_state.get("is_admin"):
        st.success(f"Logged in as Admin ({st.session_state.get('username')})")
        if st.button("Log out"):
            st.session_state["username"] = ""
            st.session_state["is_admin"] = False
        return

    st.subheader("Sign in")
    with st.form("login"):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        rows = query("SELECT username,password_hash,is_admin FROM users WHERE username=%s", (user,))
        if rows:
            ok = bcrypt.checkpw(pwd.encode("utf-8"), rows[0]["password_hash"].encode("utf-8"))
            if ok:
                st.session_state["username"] = user
                st.session_state["is_admin"] = rows[0]["is_admin"]
                if rows[0]["is_admin"]:
                    st.success("Logged in as Admin.")
                else:
                    st.info("Logged in as player (read-only).")
                return
        st.error("Invalid credentials.")
