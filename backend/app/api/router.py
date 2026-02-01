from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.habits import router as habits_router
from app.api.routes.calendar import router as calendar_router
from app.api.routes.notes import router as notes_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.backup import router as backup_router
from app.api.routes.settings import router as settings_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])

# 下面这些是占位：阶段B逐个实现
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(habits_router, prefix="/habits", tags=["Habits"])
api_router.include_router(calendar_router, prefix="/calendar", tags=["Calendar"])
api_router.include_router(notes_router, prefix="/notes", tags=["Notes"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(backup_router, prefix="/backup", tags=["Backup"])
api_router.include_router(settings_router, prefix="/settings", tags=["Settings"])
