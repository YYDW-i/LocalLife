from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("/events")
def list_events():
    return {"ok": True, "data": [], "note": "Calendar 模块将于阶段B实现"}
