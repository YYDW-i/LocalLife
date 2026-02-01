import sqlite3
from pathlib import Path

# 连接到数据库
def connect(db_path: str = 'db.sqlite'):
    # 基于当前脚本所在目录生成绝对路径
    base_dir = Path(__file__).parent.parent.parent  # 根据项目结构调整层级
    abs_db_path = base_dir / db_path
    print(f"连接数据库: {abs_db_path.resolve()}")  # 调试用：确认实际路径
    return sqlite3.connect(str(abs_db_path))
# 执行 SQL 迁移
def run_migrations():
    db_path = 'db.sqlite'
    conn = connect(db_path)
    migrations_path = Path('../../migrations/0002_health.sql')

    with open(migrations_path, 'r', encoding='utf-8') as file:
        sql = file.read()
        conn.executescript(sql)  # ✅ 正确：执行多条语句并自动提交
    
    print("数据库迁移完成")
    conn.close()

if __name__ == '__main__':
    run_migrations()
    