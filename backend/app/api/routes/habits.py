from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def list_habits():
    return {"ok": True, "data": [], "note": "Habits 模块将于阶段B实现"}
