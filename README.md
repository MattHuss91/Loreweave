# Loreweave Blank

A self-hostable, *blank* Loreweave starter you can deploy and then initialize on first run.

## What you get
- Streamlit app with admin-only editing and player read-only views
- PostgreSQL schema + calendar seed for a 10-month, 36-day/month calendar
- First-run bootstrap page to set campaign name and create the Admin
- `DATABASE_URL` based config (works with Render/Railway/Supabase/Neon/etc.)
- One-click style deploy examples for Render and Railway

## Quickstart (local)
1. Create a PostgreSQL database and grab its connection string as `DATABASE_URL` (e.g. `postgresql://user:pass@host:5432/db`).
2. `pip install -r requirements.txt`
3. Initialize schema: `psql "$DATABASE_URL" -f sql/init_db.sql && psql "$DATABASE_URL" -f sql/seed_calendar.sql`
4. Run: `streamlit run home.py`

## Environment
- `DATABASE_URL` : connection string
- `CAMPAIGN_NAME` : default campaign title (optional)
- `ADMIN_USERNAME` : bootstrap admin (optional; can set on first run)
- `ADMIN_PASSWORD` : bootstrap password (optional; ONLY for demo—use secrets manager in prod)

## Deploy
See `deploy/` for Render and Railway examples.


---

## Deploy with one click

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)  [![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template)

### Render
- Uses the `deploy/render.yaml` Blueprint to **provision Postgres** and the **web service** automatically.
- After deploy, open the app → complete the **First‑run Setup** (campaign name + admin).

### Railway
- Click the Railway button, select your repo, and add a **PostgreSQL** service (Railway templates provision this automatically).
- Set `DATABASE_URL` to the Railway Postgres internal URL (auto-populated in templates).
- Open the app → complete the **First‑run Setup**.


**Security**: Passwords are hashed with bcrypt and stored as `password_hash` in the database. Do not commit real credentials to the repo.
