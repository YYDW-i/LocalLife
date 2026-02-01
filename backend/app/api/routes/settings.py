from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def get_settings():
    return {"ok": True, "data": {}, "note": "Settings 模块将于阶段B实现"}
