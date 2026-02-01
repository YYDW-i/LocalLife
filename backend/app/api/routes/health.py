from fastapi import APIRouter
from app import __version__
from app.db.connection import connect

router = APIRouter()

@router.get("/health")
def health():
    try:
        conn = connect('db.sqlite')
        conn.execute("SELECT 1;").fetchone()
        conn.close()
        return {"status": "ok", "version": __version__}
    except Exception as e:
        return {"status": "fail", "error": str(e)}
