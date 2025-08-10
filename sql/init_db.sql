-- Core app settings and users
CREATE TABLE IF NOT EXISTS app_settings (
  id SERIAL PRIMARY KEY,
  campaign_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  is_admin BOOLEAN NOT NULL DEFAULT false
);

-- Entities
CREATE TABLE IF NOT EXISTS characters (
  character_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT,
  status TEXT,
  bio TEXT,
  is_player BOOLEAN NOT NULL DEFAULT false,
  character_img TEXT,
  editable_by TEXT
);

CREATE TABLE IF NOT EXISTS locations (
  location_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  location_img TEXT
);

CREATE TABLE IF NOT EXISTS factions (
  faction_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  alignment TEXT,
  goals TEXT,
  faction_img TEXT
);

CREATE TABLE IF NOT EXISTS campaignevents (
  event_id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  date_occurred TEXT,
  day INT,
  month INT,
  year INT,
  world_day INT,
  location_id INT REFERENCES locations(location_id) ON DELETE SET NULL,
  summary TEXT,
  full_description TEXT
);

-- Links
CREATE TABLE IF NOT EXISTS characterappearances (
  id SERIAL PRIMARY KEY,
  character_id INT NOT NULL REFERENCES characters(character_id) ON DELETE CASCADE,
  event_id INT NOT NULL REFERENCES campaignevents(event_id) ON DELETE CASCADE,
  UNIQUE(character_id, event_id)
);

CREATE TABLE IF NOT EXISTS characterfactions (
  id SERIAL PRIMARY KEY,
  character_id INT NOT NULL REFERENCES characters(character_id) ON DELETE CASCADE,
  faction_id INT NOT NULL REFERENCES factions(faction_id) ON DELETE CASCADE,
  UNIQUE(character_id, faction_id)
);

-- Basic indexes
CREATE INDEX IF NOT EXISTS idx_events_world_day ON campaignevents(world_day);
CREATE INDEX IF NOT EXISTS idx_appear_char ON characterappearances(character_id);
CREATE INDEX IF NOT EXISTS idx_appear_event ON characterappearances(event_id);
CREATE INDEX IF NOT EXISTS idx_charf_char ON characterfactions(character_id);
CREATE INDEX IF NOT EXISTS idx_charf_faction ON characterfactions(faction_id);
