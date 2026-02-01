from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app import __version__
from app.core.config import settings
from app.db.connection import ensure_data_dirs, connect
from app.db.migrations import run_migrations
from app.api.router import api_router
from app.scheduler.scheduler import start_scheduler, shutdown_scheduler


log = logging.getLogger("locallife")


class SPAStaticFiles(StaticFiles):
    """
    用于托管 Vite build 后的 SPA：
    - /assets/* 正常静态文件
    - /xxx/yyy 深链接时返回 index.html
    """
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404 and not path.startswith("api"):
            return await super().get_response("index.html", scope)
        return response


def create_app() -> FastAPI:
    app = FastAPI(title="LocalLife API", version=__version__)

    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.routes.health_profile import router as health_profile_router
    app.include_router(health_profile_router)


    # 启动时：准备目录、跑迁移、启动调度器
    @app.on_event("startup")
    def _startup():
        ensure_data_dirs()
        conn = connect(settings.db_path)
        try:
            migrations_dir = Path(__file__).resolve().parents[1] / "migrations"
            applied = run_migrations(conn, migrations_dir)
            if applied:
                log.info("Applied migrations: %s", applied)
        finally:
            conn.close()

        if settings.SCHEDULER_ENABLED:
            start_scheduler()

    @app.on_event("shutdown")
    def _shutdown():
        if settings.SCHEDULER_ENABLED:
            shutdown_scheduler()

    # 托管前端 build 产物（若存在）
    repo_root = Path(__file__).resolve().parents[2]
    dist_dir = repo_root / "frontend" / "dist"
    if dist_dir.exists():
        app.mount("/", SPAStaticFiles(directory=dist_dir, html=True), name="spa")
        log.info("Serving frontend from: %s", dist_dir)
    else:
        log.info("frontend/dist not found. Run `npm run build` in /frontend for production mode.")

    return app


app = create_app()
