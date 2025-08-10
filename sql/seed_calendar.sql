-- Default 10x36 calendar (can be replaced in first-run wizard)
INSERT INTO calendar_settings (total_months, default_days_per_month) VALUES (10, 36)
ON CONFLICT DO NOTHING;

INSERT INTO calendar_months (month_id, name, days) VALUES
  (1,'Verdanir',36),
  (2,'Emberfall',36),
  (3,'Duskwatch',36),
  (4,'Glimmerwane',36),
  (5,'Brightreach',36),
  (6,'Stormrest',36),
  (7,'Hollowshade',36),
  (8,'Deepmoor',36),
  (9,'Frostmere',36),
  (10,'Starwake',36)
ON CONFLICT (month_id) DO NOTHING;
