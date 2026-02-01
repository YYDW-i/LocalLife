from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def list_notes():
    return {"ok": True, "data": [], "note": "Notes 模块将于阶段B实现"}
