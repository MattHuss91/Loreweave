<p align="center">
  <img src="https://i.imgur.com/WEGvkz8.png" width="220" />
</p>

# Loreweave Blank

**Mission Statement**  
Loreweave is a self-hosted campaign management app for tabletop role-playing games.  
Its mission is to give GMs and players a **beautiful, interactive, and private space** to store and explore their campaign’s characters, events, locations, and factions — without needing code or third-party accounts.

---

## Quick Summary
- **Track your world** — characters, locations, factions, and events with cross-links and searchable dropdowns.
- **Detailed views** — select a single character, location, or faction to see a clean, focused profile page.
- **Stay organised** — timeline with filters, world-day ordering, and readable dates.
- **Control permissions** — GM/Admin edits everything, players edit their own characters.
- **Manage easily** — full Admin Tool for creating, editing, deleting, and linking records.
- **No-code deploy** — one-click to Render with a free Postgres DB.
- **Custom calendars** — one-time setup with your own month names and lengths.
- **Safe changes** — deletion actions ask for confirmation before they run.

---

## Deploy on Render
- Click the button below — you’ll be taken to Render.  
[![Deploy Loreweave Blank to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/MattHuss91/Loreweave)
- **Step 1:** Create a free Render account (one-time).
- **Step 2:** Click **Apply** — Render will automatically:
  - create a free **Postgres database**
  - create a **web service** running Loreweave
  - link them together via `DATABASE_URL`
- **Step 3:** Once the build finishes, open your app’s public URL.

---

## 🛠 First-Run Setup
1. Set your **Campaign Name**.
2. Create your **Admin username & password** (stored securely with bcrypt).
3. (Optional) Enter a **custom calendar** — one month per line e.g. `Verdanir 36`.
4. Start adding characters, events, locations, and factions.

---

## Admin Tool Features
- **Create, edit, and delete**:
  - Characters (with image, bio, and editable permissions)
  - Events (with world date parsing)
  - Locations
  - Factions
- **Link & unlink**:
  - Characters ↔ Events  
  - Characters ↔ Factions
- **Confirmation prompts** for all deletions to prevent mistakes.

---

## Update Alerts (Built-in)
- Set `LOREWEAVE_UPDATE_URL` on Render to:  
  `https://raw.githubusercontent.com/<YOUR-USER>/<YOUR-REPO>/main/latest.json`
- The app compares `latest.json` to its `LOCAL_VERSION` and links to `CHANGELOG.md`.

---

## About Me

I'm Matthew Husselbury, a data analyst with a background in storytelling. Loreweave is a tool I built to support my own campaigns and found it may be of use to other GMs. Feel free to use this for your own campaigns.

---

© 2025 Matthew Husselbury. All rights reserved.  
**This repository is publicly visible but is not open source.**
