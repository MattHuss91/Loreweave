-- Seed months for the 10x36 calendar (optional reference table)
CREATE TABLE IF NOT EXISTS calendar_months (
  month_id INT PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO calendar_months (month_id, name) VALUES
  (1,'Verdanir'),(2,'Emberfall'),(3,'Duskwatch'),(4,'Glimmerwane'),(5,'Brightreach'),
  (6,'Stormrest'),(7,'Hollowshade'),(8,'Deepmoor'),(9,'Frostmere'),(10,'Starwake')
ON CONFLICT (month_id) DO NOTHING;

-- Bootstrap admin if env variables provided (run manually if desired)
-- Example:
-- INSERT INTO users (username,password,is_admin) VALUES ('Admin','changeme',true);
