# backend/app/db/migrations.py

from pathlib import Path
import sqlite3
from app.core.time import now_iso

def _ensure_migrations_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS migrations (
          version TEXT PRIMARY KEY,
          applied_at TEXT NOT NULL
        );
        """
    )

def run_migrations(conn, migrations_dir):
    # 确保 migrations 表存在
    _ensure_migrations_table(conn)
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM migrations ORDER BY applied_at DESC LIMIT 1")
    row = cursor.fetchone()

    # 如果没有迁移记录，假设版本为 None
    applied_version = row[0] if row else None
    print(f"当前迁移版本: {applied_version}")
