# backend/app/db/connection.py

import sqlite3
from pathlib import Path

# 确保数据库文件夹存在
def ensure_data_dirs():
    db_path = Path("db.sqlite")  # SQLite 数据库文件
    db_path.parent.mkdir(parents=True, exist_ok=True)  # 确保数据库路径存在

# 连接到数据库
def connect(db_path: str = 'db.sqlite'):
    return sqlite3.connect(db_path)  # 连接到数据库（如果不存在会自动创建）
# ====== 新增：兼容 health_profile.py 所需的 get_conn ======

def get_db_path() -> str:
    """
    统一数据库路径入口。
    目前保持你的老行为：默认使用项目 backend 目录下的 db.sqlite。
    如果你未来想迁移到 AppData，本函数是唯一改动点。
    """
    # 仍然用你原来的默认：db.sqlite
    return "db.sqlite"


def get_conn(db_path: str | None = None) -> sqlite3.Connection:
    """
    新增的连接函数（不影响原来的 connect）。
    health_profile.py 会 import 这个函数。
    """
    if db_path is None:
        db_path = get_db_path()

    # 确保目录存在（如果未来 db_path 变成子目录，这里也能兜住）
    ensure_data_dirs()

    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # 关键：让 row["col"] / dict(row) 能工作
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
