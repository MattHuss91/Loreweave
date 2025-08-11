import os
import streamlit as st
from utils.db import query, execute
from utils.auth import login_ui
from utils.time import parse_date
from utils.ui import apply_global_styles, page_header, card, footer

st.set_page_config(page_title="Loreweave • Admin Tool", layout="centered")
apply_global_styles()
page_header("Admin Tool")

ADMIN_LOGO = "https://i.imgur.com/YBozTrh.png"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Lora&display=swap');
.stApp {{
    background: #000000;
    font-family: 'Lora', serif !important;
    color: #FFFFFF !important;
}}
label {{
    color: #FFFFFF !important;
    font-weight: bold;
}}
div.stButton > button {{
    background-color: #333333 !important;
    color: #ffffff !important;
    font-weight: bold !important;
    font-family: 'Cinzel', serif !important;
    border: none !important;
    padding: 0.5rem 1rem !important;
    border-radius: 5px !important;
}}
.lw-footer {{
    text-align:center; font-size: 12px; margin-top: 2rem; opacity: 0.9; color: #fff;
}}
</style>
<div style='text-align: center; margin-top: -20px;'>
    <img src='{ADMIN_LOGO}' style='width: 200px; margin-bottom: -10px;' />
    <h1 style='margin-top: 0; font-family: "Cinzel", serif; text-transform: uppercase; color: #fff;'>Admin Tool</h1>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Connected to:")
    host = os.getenv("DATABASE_URL","").split("@")[-1] if os.getenv("DATABASE_URL") else "(not set)"
    st.code(host or "(unknown)")

login_ui()
if not st.session_state.get("is_admin"):
    st.warning("Admin only.")
    st.stop()

mode = st.sidebar.selectbox("WHAT WOULD YOU LIKE TO MANAGE?", [
    "Characters", "Events", "Locations", "Factions", "Users", "Link Character to Event", "Link Character to Faction"
])

def get_all(table, id_col, name_col, order_col=None):
    oc = order_col or name_col
    rows = query(f"SELECT {id_col} AS id, {name_col} AS name FROM {table} ORDER BY {oc}")
    return [(r["id"], r["name"]) for r in rows]

# -------- delete confirm helper --------
def confirm_delete(key: str, noun: str) -> bool:
    ask_key = f"ask_{key}"
    yes_key = f"yes_{key}"
    no_key = f"no_{key}"

    if st.button(f"🗑️ Delete {noun}", key=f"start_{key}"):
        st.session_state[ask_key] = True

    if st.session_state.get(ask_key):
        st.warning(f"Are you sure you want to permanently delete this {noun.lower()}? This cannot be undone.")
        col1, col2 = st.columns(2)
        yes = col1.button("Yes, delete", key=yes_key)
        cancel = col2.button("Cancel", key=no_key)
        if yes:
            st.session_state.pop(ask_key, None)
            return True
        if cancel:
            st.session_state.pop(ask_key, None)
    return False

# ---------------- Characters ----------------
if mode == "Characters":
    sub = st.radio("Action", ["Create", "Edit", "Delete"], horizontal=True)

    if sub == "Create":
        with st.form("c_new"):
            name = st.text_input("Name")
            ctype = st.text_input("Type")
            status = st.text_input("Status", value="Alive")
            bio = st.text_area("Bio")
            is_player = st.checkbox("Is Player?")
            img = st.text_input("Image URL")
            editable_by = st.text_input("Editable by (username)")
            if st.form_submit_button("Create"):
                execute("""INSERT INTO characters (name, type, status, bio, is_player, character_img, editable_by)
                           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                        (name, ctype, status, bio, is_player, img, editable_by or None))
                st.success("Character created.")

    elif sub == "Edit":
        chars = get_all("characters", "character_id", "name")
        if not chars:
            st.info("No characters yet."); st.stop()
        id_by_name = {n:i for i,n in chars}
        selected = st.selectbox("Select character", [n for _,n in chars])
        cid = id_by_name[selected]
        row = query("""SELECT name,type,status,bio,is_player,character_img,editable_by
                       FROM characters WHERE character_id=%s""",[cid])[0]
        with st.form("c_edit"):
            name = st.text_input("Name", value=row["name"])
            ctype = st.text_input("Type", value=row["type"] or "")
            status = st.text_input("Status", value=row["status"] or "")
            bio = st.text_area("Bio", value=row["bio"] or "")
            is_player = st.checkbox("Is Player?", value=row["is_player"])
            img = st.text_input("Image URL", value=row["character_img"] or "")
            editable_by = st.text_input("Editable by (username)", value=row["editable_by"] or "")
            if st.form_submit_button("Update"):
                execute("""UPDATE characters SET name=%s,type=%s,status=%s,bio=%s,is_player=%s,character_img=%s,editable_by=%s
                           WHERE character_id=%s""",
                        (name, ctype, status, bio, is_player, img, editable_by or None, cid))
                st.success("Updated.")

    else:  # Delete
        chars = get_all("characters", "character_id", "name")
        if not chars:
            st.info("No characters yet."); st.stop()
        id_by_name = {n:i for i,n in chars}
        selected = st.selectbox("Select character to delete", [n for _,n in chars])
        cid = id_by_name[selected]

        if confirm_delete(f"char_{cid}", "Character"):
            # remove links then the character
            execute("DELETE FROM characterappearances WHERE character_id=%s", (cid,))
            execute("DELETE FROM characterfactions   WHERE character_id=%s", (cid,))
            execute("DELETE FROM characters WHERE character_id=%s", (cid,))
            st.success("Character deleted.")
            st.rerun()

# ---------------- Events ----------------
elif mode == "Events":
    sub = st.radio("Action", ["Create", "Edit", "Delete"], horizontal=True)
    locs = get_all("locations", "location_id", "name")
    loc_name_to_id = {n:i for i,n in locs}

    if sub == "Create":
        with st.form("e_new"):
            title = st.text_input("Title")
            date_text = st.text_input("Date (e.g., 12 Glimmerwane 104)")
            location = st.selectbox("Location", [""] + [n for _,n in locs])
            summary = st.text_area("Summary")
            full = st.text_area("Full Description")
            if st.form_submit_button("Create"):
                day, month, year, world_day = parse_date(date_text)
                loc_id = loc_name_to_id.get(location)
                execute("""INSERT INTO campaignevents (title,date_occurred,day,month,year,world_day,location_id,summary,full_description)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (title, date_text, day, month, year, world_day, loc_id, summary, full))
                st.success("Event created.")

    elif sub == "Edit":
        events = get_all("campaignevents", "event_id", "title", order_col="world_day")
        if not events:
            st.info("No events yet."); st.stop()
        id_by_name = {n:i for i,n in events}
        selected = st.selectbox("Select event", [n for _,n in events])
        eid = id_by_name[selected]
        row = query("""SELECT title,date_occurred,location_id,summary,full_description
                       FROM campaignevents WHERE event_id=%s""",[eid])[0]
        with st.form("e_edit"):
            title = st.text_input("Title", value=row["title"])
            date_text = st.text_input("Date", value=row["date_occurred"] or "")
            location_names = [""] + [n for _,n in locs]
            current_loc = next((n for n,i in loc_name_to_id.items() if i==row["location_id"]), "")
            location = st.selectbox("Location", location_names,
                                    index=location_names.index(current_loc) if current_loc in location_names else 0)
            summary = st.text_area("Summary", value=row["summary"] or "")
            full = st.text_area("Full Description", value=row["full_description"] or "")
            if st.form_submit_button("Update"):
                day, month, year, world_day = parse_date(date_text)
                loc_id = loc_name_to_id.get(location)
                execute("""UPDATE campaignevents
                           SET title=%s,date_occurred=%s,day=%s,month=%s,year=%s,world_day=%s,location_id=%s,summary=%s,full_description=%s
                           WHERE event_id=%s""",
                        (title, date_text, day, month, year, world_day, loc_id, summary, full, eid))
                st.success("Updated.")

    else:  # Delete
        events = get_all("campaignevents", "event_id", "title", order_col="world_day")
        if not events:
            st.info("No events yet."); st.stop()
        id_by_name = {n:i for i,n in events}
        selected = st.selectbox("Select event to delete", [n for _,n in events])
        eid = id_by_name[selected]

        if confirm_delete(f"event_{eid}", "Event"):
            execute("DELETE FROM characterappearances WHERE event_id=%s", (eid,))
            execute("DELETE FROM campaignevents WHERE event_id=%s", (eid,))
            st.success("Event deleted.")
            st.rerun()

# ---------------- Locations ----------------
elif mode == "Locations":
    sub = st.radio("Action", ["Create", "Edit", "Delete"], horizontal=True)

    if sub == "Create":
        with st.form("l_new"):
            name = st.text_input("Name")
            desc = st.text_area("Description")
            img = st.text_input("Image URL")
            if st.form_submit_button("Create"):
                execute("INSERT INTO locations (name, description, location_img) VALUES (%s,%s,%s)", (name, desc, img))
                st.success("Location created.")

    elif sub == "Edit":
        locs = get_all("locations", "location_id", "name")
        if not locs:
            st.info("No locations yet."); st.stop()
        id_by_name = {n:i for i,n in locs}
        selected = st.selectbox("Select location", [n for _,n in locs])
        lid = id_by_name[selected]
        row = query("SELECT name,description,location_img FROM locations WHERE location_id=%s",[lid])[0]
        with st.form("l_edit"):
            name = st.text_input("Name", value=row["name"])
            desc = st.text_area("Description", value=row["description"] or "")
            img = st.text_input("Image URL", value=row["location_img"] or "")
            if st.form_submit_button("Update"):
                execute("UPDATE locations SET name=%s,description=%s,location_img=%s WHERE location_id=%s",
                        (name, desc, img, lid))
                st.success("Updated.")

    else:  # Delete
        locs = get_all("locations", "location_id", "name")
        if not locs:
            st.info("No locations yet."); st.stop()
        id_by_name = {n:i for i,n in locs}
        selected = st.selectbox("Select location to delete", [n for _,n in locs])
        lid = id_by_name[selected]

        if confirm_delete(f"loc_{lid}", "Location"):
            # detach events first, then delete location
            execute("UPDATE campaignevents SET location_id=NULL WHERE location_id=%s", (lid,))
            execute("DELETE FROM locations WHERE location_id=%s", (lid,))
            st.success("Location deleted.")
            st.rerun()

# ---------------- Factions ----------------
elif mode == "Factions":
    sub = st.radio("Action", ["Create", "Edit", "Delete"], horizontal=True)

    if sub == "Create":
        with st.form("f_new"):
            name = st.text_input("Name")
            ali = st.text_input("Alignment")
            goals = st.text_area("Goals/Description")
            img = st.text_input("Image URL")
            if st.form_submit_button("Create"):
                execute("INSERT INTO factions (name, alignment, goals, faction_img) VALUES (%s,%s,%s,%s)",
                        (name, ali, goals, img))
                st.success("Faction created.")

    elif sub == "Edit":
        facs = get_all("factions", "faction_id", "name")
        if not facs:
            st.info("No factions yet."); st.stop()
        id_by_name = {n:i for i,n in facs}
        selected = st.selectbox("Select faction", [n for _,n in facs])
        fid = id_by_name[selected]
        row = query("SELECT name,alignment,goals,faction_img FROM factions WHERE faction_id=%s",[fid])[0]
        with st.form("f_edit"):
            name = st.text_input("Name", value=row["name"])
            ali = st.text_input("Alignment", value=row["alignment"] or "")
            goals = st.text_area("Goals/Description", value=row["goals"] or "")
            img = st.text_input("Image URL", value=row["faction_img"] or "")
            if st.form_submit_button("Update"):
                execute("UPDATE factions SET name=%s,alignment=%s,goals=%s,faction_img=%s WHERE faction_id=%s",
                        (name, ali, goals, img, fid))
                st.success("Updated.")

    else:  # Delete
        facs = get_all("factions", "faction_id", "name")
        if not facs:
            st.info("No factions yet."); st.stop()
        id_by_name = {n:i for i,n in facs}
        selected = st.selectbox("Select faction to delete", [n for _,n in facs])
        fid = id_by_name[selected]

        if confirm_delete(f"fac_{fid}", "Faction"):
            execute("DELETE FROM characterfactions WHERE faction_id=%s", (fid,))
            execute("DELETE FROM factions WHERE faction_id=%s", (fid,))
            st.success("Faction deleted.")
            st.rerun()

# ---------------- Users ----------------
elif mode == "Users":
    st.caption("Create players or additional admins.")
    sub = st.radio("Action", ["Create", "List", "Delete"], horizontal=True)

    if sub == "Create":
        with st.form("u_new"):
            uname = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            is_admin = st.checkbox("Is Admin?", value=False)
            if st.form_submit_button("Create User"):
                import bcrypt
                pw_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                execute("INSERT INTO users (username,password_hash,is_admin) VALUES (%s,%s,%s)",
                        (uname, pw_hash, is_admin))
                st.success("User created.")

    elif sub == "List":
        rows = query("SELECT username,is_admin FROM users ORDER BY username")
        if not rows:
            st.info("No users yet.")
        else:
            for r in rows:
                st.write(f"- **{r['username']}** — {'Admin' if r['is_admin'] else 'Player'}")

    else:  # Delete user
        users = query("SELECT username, is_admin FROM users ORDER BY username")
        if not users:
            st.info("No users yet."); st.stop()
        chosen = st.selectbox("Select user to delete", [u["username"] for u in users])
        target = next(u for u in users if u["username"] == chosen)

        if target["is_admin"] and len([u for u in users if u["is_admin"]]) <= 1:
            st.warning("You cannot delete the last remaining admin.")
        else:
            if confirm_delete(f"user_{chosen}", "User"):
                execute("DELETE FROM users WHERE username=%s", (chosen,))
                st.success("User deleted.")
                st.rerun()

# ---------------- Linking ----------------
elif mode == "Link Character to Event":
    # --- create link ---
    chars = get_all("characters","character_id","name")
    evs = get_all("campaignevents","event_id","title")
    idc = {n:i for i,n in chars}
    ide = {n:i for i,n in evs}
    with st.form("link_c_e"):
        char = st.selectbox("Character", [n for _,n in chars], key="lk_ce_char")
        ev = st.selectbox("Event", [n for _,n in evs], key="lk_ce_event")
        if st.form_submit_button("Link"):
            execute(
                "INSERT INTO characterappearances (character_id,event_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                (idc[char], ide[ev])
            )
            st.success("Linked.")

    st.markdown("<div class='lw-hr'></div>", unsafe_allow_html=True)

    # --- unlink existing ---
    links = query("""
        SELECT ca.character_id, c.name AS character, ca.event_id, e.title AS event
        FROM characterappearances ca
        JOIN characters c ON c.character_id = ca.character_id
        JOIN campaignevents e ON e.event_id = ca.event_id
        ORDER BY c.name, e.world_day, e.title
    """)
    if links:
        char_names = sorted({r["character"] for r in links})
        picked_char = st.selectbox("Character (linked)", char_names, key="ul_ce_char")
        ev_for_char = [r for r in links if r["character"] == picked_char]
        ev_names = [r["event"] for r in ev_for_char]
        picked_event = st.selectbox("Event to unlink", ev_names, key="ul_ce_event")

        # find ids for picked pair
        pair = next(r for r in ev_for_char if r["event"] == picked_event)
        if confirm_delete(f"unlink_ce_{pair['character_id']}_{pair['event_id']}", "Link"):
            execute("DELETE FROM characterappearances WHERE character_id=%s AND event_id=%s",
                    (pair["character_id"], pair["event_id"]))
            st.success("Link removed.")
            st.rerun()
    else:
        st.info("No character ↔ event links yet.")

elif mode == "Link Character to Faction":
    # --- create link ---
    chars = get_all("characters","character_id","name")
    facs  = get_all("factions","faction_id","name")
    idc = {n:i for i,n in chars}
    idf = {n:i for i,n in facs}
    with st.form("link_c_f"):
        char = st.selectbox("Character", [n for _,n in chars], key="lk_cf_char")
        fac  = st.selectbox("Faction",  [n for _,n in facs],  key="lk_cf_faction")
        if st.form_submit_button("Link"):
            execute(
                "INSERT INTO characterfactions (character_id,faction_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                (idc[char], idf[fac])
            )
            st.success("Linked.")

    st.markdown("<div class='lw-hr'></div>", unsafe_allow_html=True)

    # --- unlink existing ---
    links = query("""
        SELECT cf.character_id, c.name AS character, cf.faction_id, f.name AS faction
        FROM characterfactions cf
        JOIN characters c ON c.character_id = cf.character_id
        JOIN factions  f ON f.faction_id  = cf.faction_id
        ORDER BY c.name, f.name
    """)
    if links:
        char_names = sorted({r["character"] for r in links})
        picked_char = st.selectbox("Character (linked)", char_names, key="ul_cf_char")
        fac_for_char = [r for r in links if r["character"] == picked_char]
        fac_names = [r["faction"] for r in fac_for_char]
        picked_faction = st.selectbox("Faction to unlink", fac_names, key="ul_cf_faction")

        pair = next(r for r in fac_for_char if r["faction"] == picked_faction)
        if confirm_delete(f"unlink_cf_{pair['character_id']}_{pair['faction_id']}", "Link"):
            execute("DELETE FROM characterfactions WHERE character_id=%s AND faction_id=%s",
                    (pair["character_id"], pair["faction_id"]))
            st.success("Link removed.")
            st.rerun()
    else:
        st.info("No character ↔ faction links yet.")

st.markdown("<div class='lw-footer'>Powered by Loreweave • © 2025 Matthew Husselbury</div>", unsafe_allow_html=True)
