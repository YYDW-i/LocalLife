from fastapi import APIRouter
from app.db.connection import connect

router = APIRouter()

@router.get("/tasks/today")
def get_today_tasks():
    try:
        conn = connect('db.sqlite')
        query = """
        SELECT * FROM tasks
        WHERE due_date = CURRENT_DATE
        """
        tasks = conn.execute(query).fetchall()
        conn.close()
        return {"tasks": tasks}
    except Exception as e:
        return {"error": str(e)}
