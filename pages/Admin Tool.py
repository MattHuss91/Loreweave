import os
import streamlit as st
from utils.db import query, execute
from utils.auth import login_ui
from utils.time import parse_date
from utils.ui import apply_global_styles, page_header

# --- Streamlit config ---
st.set_page_config(page_title="Loreweave • Admin Tool", layout="centered")
apply_global_styles()
page_header("Admin Tool")

ADMIN_LOGO = "https://i.imgur.com/YBozTrh.png"

# --- Sidebar connection info ---
with st.sidebar:
    st.markdown("### Connected to:")
    host = os.getenv("DATABASE_URL","").split("@")[-1] if os.getenv("DATABASE_URL") else "(not set)"
    st.code(host or "(unknown)")

# --- Login check ---
login_ui()
if not st.session_state.get("is_admin"):
    st.warning("Admin only.")
    st.stop()

# --- Mode selector ---
mode = st.sidebar.selectbox("WHAT WOULD YOU LIKE TO MANAGE?", [
    "Characters", "Events", "Locations", "Factions", "Users",
    "Link Character to Event", "Link Character to Faction"
])

def get_all(table, id_col, name_col, order_col=None):
    oc = order_col or name_col
    rows = query(f"SELECT {id_col} AS id, {name_col} AS name FROM {table} ORDER BY {oc}")
    return [(r["id"], r["name"]) for r in rows]

# ---------------- Characters ----------------
if mode == "Characters":
    sub = st.radio("Action", ["Create", "Edit"], horizontal=True)

    if sub == "Create":
        with st.form("c_new"):
            name = st.text_input("Name")
            ctype = st.text_input("Type")
            status = st.text_input("Status", value="Alive")
            bio = st.text_area("Bio")
            is_player = st.checkbox("Is Player?")
            img = st.text_input("Image URL")
            editable_by = st.text_input("Editable by (username)")
            create = st.form_submit_button("Create")
            if create:
                execute(
                    """INSERT INTO characters (name, type, status, bio, is_player, character_img, editable_by)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (name, ctype, status, bio, is_player, img, editable_by or None)
                )
                st.success("Character created.")

    else:  # Edit (and Delete in same form)
        chars = get_all("characters", "character_id", "name")
        if not chars:
            st.info("No characters yet."); st.stop()
        id_by_name = {n:i for i,n in chars}
        selected = st.selectbox("Select character", [n for _,n in chars])
        cid = id_by_name[selected]
        row = query(
            "SELECT name,type,status,bio,is_player,character_img,editable_by FROM characters WHERE character_id=%s",
            [cid]
        )[0]

        with st.form(f"c_edit_{cid}"):
            name = st.text_input("Name", value=row["name"])
            ctype = st.text_input("Type", value=row["type"] or "")
            status = st.text_input("Status", value=row["status"] or "")
            bio = st.text_area("Bio", value=row["bio"] or "")
            is_player = st.checkbox("Is Player?", value=row["is_player"])
            img = st.text_input("Image URL", value=row["character_img"] or "")
            editable_by = st.text_input("Editable by (username)", value=row["editable_by"] or "")

            confirm_del = st.checkbox("Yes, I’m sure I want to delete this character (and its links).")
            col1, col2 = st.columns(2)
            upd = col1.form_submit_button("Update")
            dele = col2.form_submit_button("Delete")

            if upd:
                execute(
                    """UPDATE characters SET name=%s,type=%s,status=%s,bio=%s,is_player=%s,character_img=%s,editable_by=%s
                       WHERE character_id=%s""",
                    (name, ctype, status, bio, is_player, img, editable_by or None, cid)
                )
                st.success("Character updated.")

            if dele:
                if not confirm_del:
                    st.warning("Tick the confirmation box to delete.")
                else:
                    execute("DELETE FROM characterappearances WHERE character_id=%s", (cid,))
                    execute("DELETE FROM characterfactions   WHERE character_id=%s", (cid,))
                    execute("DELETE FROM characters WHERE character_id=%s", (cid,))
                    st.success("Character deleted.")
                    st.rerun()

# ---------------- Events ----------------
elif mode == "Events":
    sub = st.radio("Action", ["Create", "Edit"], horizontal=True)
    locs = get_all("locations", "location_id", "name")
    loc_name_to_id = {n:i for i,n in locs}

    if sub == "Create":
        with st.form("e_new"):
            title = st.text_input("Title")
            date_text = st.text_input("Date (e.g., 12 Glimmerwane 104)")
            location = st.selectbox("Location", [""] + [n for _,n in locs])
            summary = st.text_area("Summary")
            full = st.text_area("Full Description")
            create = st.form_submit_button("Create")
            if create:
                day, month, year, world_day = parse_date(date_text)
                loc_id = loc_name_to_id.get(location)
                execute(
                    """INSERT INTO campaignevents (title,date_occurred,day,month,year,world_day,location_id,summary,full_description)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (title, date_text, day, month, year, world_day, loc_id, summary, full)
                )
                st.success("Event created.")
    else:
        events = get_all("campaignevents", "event_id", "title", order_col="world_day")
        if not events:
            st.info("No events yet."); st.stop()
        id_by_name = {n:i for i,n in events}
        selected = st.selectbox("Select event", [n for _,n in events])
        eid = id_by_name[selected]
        row = query(
            "SELECT title,date_occurred,location_id,summary,full_description FROM campaignevents WHERE event_id=%s",
            [eid]
        )[0]

        with st.form(f"e_edit_{eid}"):
            title = st.text_input("Title", value=row["title"])
            date_text = st.text_input("Date", value=row["date_occurred"] or "")
            location_names = [""] + [n for _,n in locs]
            current_loc = next((n for n,i in loc_name_to_id.items() if i==row["location_id"]), "")
            location = st.selectbox(
                "Location", location_names,
                index=location_names.index(current_loc) if current_loc in location_names else 0
            )
            summary = st.text_area("Summary", value=row["summary"] or "")
            full = st.text_area("Full Description", value=row["full_description"] or "")

            confirm_del = st.checkbox("Yes, I’m sure I want to delete this event (and its links).")
            col1, col2 = st.columns(2)
            upd = col1.form_submit_button("Update")
            dele = col2.form_submit_button("Delete")

            if upd:
                day, month, year, world_day = parse_date(date_text)
                loc_id = loc_name_to_id.get(location)
                execute(
                    """UPDATE campaignevents
                       SET title=%s,date_occurred=%s,day=%s,month=%s,year=%s,world_day=%s,location_id=%s,summary=%s,full_description=%s
                       WHERE event_id=%s""",
                    (title, date_text, day, month, year, world_day, loc_id, summary, full, eid)
                )
                st.success("Event updated.")

            if dele:
                if not confirm_del:
                    st.warning("Tick the confirmation box to delete.")
                else:
                    execute("DELETE FROM characterappearances WHERE event_id=%s", (eid,))
                    execute("DELETE FROM campaignevents WHERE event_id=%s", (eid,))
                    st.success("Event deleted.")
                    st.rerun()

# ---------------- Locations ----------------
elif mode == "Locations":
    sub = st.radio("Action", ["Create", "Edit"], horizontal=True)

    if sub == "Create":
        with st.form("l_new"):
            name = st.text_input("Name")
            desc = st.text_area("Description")
            img = st.text_input("Image URL")
            create = st.form_submit_button("Create")
            if create:
                execute("INSERT INTO locations (name, description, location_img) VALUES (%s,%s,%s)", (name, desc, img))
                st.success("Location created.")

    else:
        locs = get_all("locations", "location_id", "name")
        if not locs:
            st.info("No locations yet."); st.stop()
        id_by_name = {n:i for i,n in locs}
        selected = st.selectbox("Select location", [n for _,n in locs])
        lid = id_by_name[selected]
        row = query("SELECT name,description,location_img FROM locations WHERE location_id=%s",[lid])[0]

        with st.form(f"l_edit_{lid}"):
            name = st.text_input("Name", value=row["name"])
            desc = st.text_area("Description", value=row["description"] or "")
            img = st.text_input("Image URL", value=row["location_img"] or "")

            confirm_del = st.checkbox("Yes, I’m sure I want to delete this location.")
            col1, col2 = st.columns(2)
            upd = col1.form_submit_button("Update")
            dele = col2.form_submit_button("Delete")

            if upd:
                execute(
                    "UPDATE locations SET name=%s,description=%s,location_img=%s WHERE location_id=%s",
                    (name, desc, img, lid)
                )
                st.success("Location updated.")

            if dele:
                if not confirm_del:
                    st.warning("Tick the confirmation box to delete.")
                else:
                    # detach related events first to avoid FK issues
                    execute("UPDATE campaignevents SET location_id=NULL WHERE location_id=%s", (lid,))
                    execute("DELETE FROM locations WHERE location_id=%s", (lid,))
                    st.success("Location deleted.")
                    st.rerun()

# ---------------- Factions ----------------
elif mode == "Factions":
    sub = st.radio("Action", ["Create", "Edit"], horizontal=True)

    if sub == "Create":
        with st.form("f_new"):
            name = st.text_input("Name")
            ali = st.text_input("Alignment")
            goals = st.text_area("Goals/Description")
            img = st.text_input("Image URL")
            create = st.form_submit_button("Create")
            if create:
                execute(
                    "INSERT INTO factions (name, alignment, goals, faction_img) VALUES (%s,%s,%s,%s)",
                    (name, ali, goals, img)
                )
                st.success("Faction created.")

    else:
        facs = get_all("factions", "faction_id", "name")
        if not facs:
            st.info("No factions yet."); st.stop()
        id_by_name = {n:i for i,n in facs}
        selected = st.selectbox("Select faction", [n for _,n in facs])
        fid = id_by_name[selected]
        row = query("SELECT name,alignment,goals,faction_img FROM factions WHERE faction_id=%s",[fid])[0]

        with st.form(f"f_edit_{fid}"):
            name = st.text_input("Name", value=row["name"])
            ali = st.text_input("Alignment", value=row["alignment"] or "")
            goals = st.text_area("Goals/Description", value=row["goals"] or "")
            img = st.text_input("Image URL", value=row["faction_img"] or "")

            confirm_del = st.checkbox("Yes, I’m sure I want to delete this faction (and its links).")
            col1, col2 = st.columns(2)
            upd = col1.form_submit_button("Update")
            dele = col2.form_submit_button("Delete")

            if upd:
                execute(
                    "UPDATE factions SET name=%s,alignment=%s,goals=%s,faction_img=%s WHERE faction_id=%s",
                    (name, ali, goals, img, fid)
                )
                st.success("Faction updated.")

            if dele:
                if not confirm_del:
                    st.warning("Tick the confirmation box to delete.")
                else:
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
            create = st.form_submit_button("Create User")
            if create:
                import bcrypt
                pw_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                execute(
                    "INSERT INTO users (username,password_hash,is_admin) VALUES (%s,%s,%s)",
                    (uname, pw_hash, is_admin)
                )
                st.success("User created.")

    elif sub == "List":
        rows = query("SELECT username,is_admin FROM users ORDER BY username")
        if not rows:
            st.info("No users yet.")
        else:
            for r in rows:
                st.write(f"- **{r['username']}** — {'Admin' if r['is_admin'] else 'Player'}")

    else:  # Delete
        users = query("SELECT username, is_admin FROM users ORDER BY username")
        if not users:
            st.info("No users yet."); st.stop()
        chosen = st.selectbox("Select user to delete", [u["username"] for u in users])
        target = next(u for u in users if u["username"] == chosen)

        with st.form(f"user_del_{chosen}"):
            confirm_del = st.checkbox("Yes, I’m sure I want to delete this user.")
            dele = st.form_submit_button("Delete User")
            if dele:
                if target["is_admin"] and len([u for u in users if u["is_admin"]]) <= 1:
                    st.warning("You cannot delete the last remaining admin.")
                elif not confirm_del:
                    st.warning("Tick the confirmation box to delete.")
                else:
                    execute("DELETE FROM users WHERE username=%s", (chosen,))
                    st.success("User deleted.")
                    st.rerun()

# ---------------- Link Character to Event ----------------
elif mode == "Link Character to Event":
    chars = get_all("characters","character_id","name")
    evs = get_all("campaignevents","event_id","title")
    idc = {n:i for i,n in chars}
    ide = {n:i for i,n in evs}

    with st.form("link_c_e"):
        char = st.selectbox("Character", [n for _,n in chars], key="lk_ce_char")
        ev = st.selectbox("Event", [n for _,n in evs], key="lk_ce_event")
        col1, col2 = st.columns(2)
        link_btn = col1.form_submit_button("Link")
        del_btn  = col2.form_submit_button("Delete Link")
        confirm_del = st.checkbox("Yes, I’m sure I want to delete this link.")

        if link_btn:
            execute(
                "INSERT INTO characterappearances (character_id,event_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                (idc[char], ide[ev])
            )
            st.success("Linked.")

        if del_btn:
            if not confirm_del:
                st.warning("Tick the confirmation box to delete.")
            else:
                execute(
                    "DELETE FROM characterappearances WHERE character_id=%s AND event_id=%s",
                    (idc[char], ide[ev])
                )
                st.success("Link deleted.")
                st.rerun()

# ---------------- Link Character to Faction ----------------
elif mode == "Link Character to Faction":
    chars = get_all("characters","character_id","name")
    facs = get_all("factions","faction_id","name")
    idc = {n:i for i,n in chars}
    idf = {n:i for i,n in facs}

    with st.form("link_c_f"):
        char = st.selectbox("Character", [n for _,n in chars], key="lk_cf_char")
        fac  = st.selectbox("Faction",  [n for _,n in facs],  key="lk_cf_faction")
        col1, col2 = st.columns(2)
        link_btn = col1.form_submit_button("Link")
        del_btn  = col2.form_submit_button("Delete Link")
        confirm_del = st.checkbox("Yes, I’m sure I want to delete this link.")

        if link_btn:
            execute(
                "INSERT INTO characterfactions (character_id,faction_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                (idc[char], idf[fac])
            )
            st.success("Linked.")

        if del_btn:
            if not confirm_del:
                st.warning("Tick the confirmation box to delete.")
            else:
                execute(
                    "DELETE FROM characterfactions WHERE character_id=%s AND faction_id=%s",
                    (idc[char], idf[fac])
                )
                st.success("Link deleted.")
                st.rerun()

# --- Footer ---
st.caption("Powered by Loreweave • © 2025 Matthew Husselbury")
