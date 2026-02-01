from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def backup_root():
    return {"ok": True, "data": {}, "note": "Backup/Restore 模块将于阶段B实现"}
