# backend/init_db.py

from app.db.create_tables import create_tables  # 导入创建表的函数

if __name__ == "__main__":
    create_tables()  # 执行表创建操作
    print("数据库和任务表已创建成功！")
