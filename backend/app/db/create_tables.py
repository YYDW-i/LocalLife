# backend/app/db/create_tables.py

from .connection import connect

def create_tables():
    conn = connect('db.sqlite')  # 连接数据库
    cursor = conn.cursor()
    
    # 创建任务表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,  -- 任务名称
            due_date DATE NOT NULL,  -- 任务到期日期
            priority INTEGER DEFAULT 1  -- 任务优先级
        );
    ''')
    
    conn.commit()  # 提交数据库事务
    conn.close()  # 关闭数据库连接
