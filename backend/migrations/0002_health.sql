-- 0002_health.sql
-- 健康资料（手动输入） + 体重记录（可选）

CREATE TABLE IF NOT EXISTS health_profile (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  height_cm REAL,              -- 身高（cm）
  weight_kg REAL,              -- 当前体重（kg）
  age_years INTEGER,           -- 年龄（岁）
  sex TEXT,                    -- 'male' | 'female' | 'unspecified'
  activity_level TEXT,         -- 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active'
  updated_at TEXT NOT NULL
);

INSERT OR IGNORE INTO health_profile
(id, height_cm, weight_kg, age_years, sex, activity_level, updated_at)
VALUES
(1, NULL, NULL, NULL, 'unspecified', 'sedentary', datetime('now'));

CREATE TABLE IF NOT EXISTS health_weight_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  weight_kg REAL NOT NULL,
  logged_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_health_weight_logs_logged_at
ON health_weight_logs (logged_at);
