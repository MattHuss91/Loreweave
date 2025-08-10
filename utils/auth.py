import os
import streamlit as st
from .db import query, execute, run_sql_file
import bcrypt

SCHEMA_OK_KEY = "schema_ok"
INITIALIZED_KEY = "initialized"

def ensure_bootstrap():
    """
    Ensures the database schema exists and basic app_settings row is present.
    If schema is missing, attempts to create it from sql/init_db.sql & seed_calendar.sql.
    Sets st.session_state flags:
      - SCHEMA_OK_KEY: schema tables exist
      - INITIALIZED_KEY: app_settings exists and at least 1 admin user exists
    """
    # Quick table check
    try:
        _ = query("SELECT 1 FROM information_schema.tables WHERE table_name='app_settings'")
    except Exception:
        st.error("Cannot connect to the database. Make sure DATABASE_URL is set and reachable.")
        st.stop()

    # Does schema exist?
    app_settings_tbl = query("""SELECT table_name FROM information_schema.tables WHERE table_name='app_settings'""")
    if not app_settings_tbl:
        # Try to auto-initialize from bundled SQL files
        sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sql")
        init_sql = os.path.join(sql_dir, "init_db.sql")
        seed_sql = os.path.join(sql_dir, "seed_calendar.sql")
        try:
            run_sql_file(init_sql)
            run_sql_file(seed_sql)
            st.success("Database initialized.")
        except Exception as e:
            st.error(f"Failed to initialize DB schema automatically. Error: {e}")
            st.stop()

    st.session_state[SCHEMA_OK_KEY] = True

    # Ensure one app_settings row
    rows = query("SELECT * FROM app_settings")
    if not rows:
        campaign_name = os.getenv("CAMPAIGN_NAME", None)
        if campaign_name:
            execute("INSERT INTO app_settings (campaign_name) VALUES (%s)", (campaign_name,))
    # Check admin presence
    admins = query("SELECT 1 FROM users WHERE is_admin=true LIMIT 1")
    st.session_state[INITIALIZED_KEY] = bool(query("SELECT 1 FROM app_settings LIMIT 1")) and bool(admins)

def show_first_run_wizard():
    """
    UI for first-time setup: set campaign name and create Admin user.
    Returns True once completed.
    """
    st.header("First‑run Setup")
    st.write("Name your campaign and create the Admin account.")

    with st.form("first_run"):
        cname = st.text_input("Campaign name", placeholder="Your Campaign")
        user = st.text_input("Admin username", value="Admin")
        pwd = st.text_input("Admin password", type="password")
        ok = st.form_submit_button("Initialize")
    if ok:
        if not cname or not user or not pwd:
            st.error("Please fill all fields.")
            return False
        execute("INSERT INTO app_settings (campaign_name) VALUES (%s)", (cname,))
        pw_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        execute("INSERT INTO users (username,password_hash,is_admin) VALUES (%s,%s,true)", (user, pw_hash))
        st.success("Initialized! You can now log in as Admin.")
        st.session_state[INITIALIZED_KEY] = True
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
        if rows and bcrypt.checkpw(pwd.encode("utf-8"), rows[0]["password_hash"].encode("utf-8")):
            st.session_state["username"] = user
            st.session_state["is_admin"] = rows[0]["is_admin"]
            if rows[0]["is_admin"]:
                st.success("Logged in as Admin.")
            else:
                st.info("Logged in as player (read-only).")
        else:
            st.error("Invalid credentials.")
