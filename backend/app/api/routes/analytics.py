from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def analytics_root():
    return {"ok": True, "data": {}, "note": "Analytics 模块将于阶段B实现"}
