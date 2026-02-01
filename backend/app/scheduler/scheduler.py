from __future__ import annotations

import logging
from apscheduler.schedulers.background import BackgroundScheduler

log = logging.getLogger("locallife.scheduler")

_scheduler: BackgroundScheduler | None = None


def start_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        return

    scheduler = BackgroundScheduler(timezone="UTC")

    # 阶段A：放一个“心跳”任务，证明调度器正常工作
    def heartbeat():
        log.info("scheduler heartbeat")

    scheduler.add_job(heartbeat, "interval", minutes=60, id="heartbeat", replace_existing=True)
    scheduler.start()

    _scheduler = scheduler
    log.info("APScheduler started")


def shutdown_scheduler() -> None:
    global _scheduler
    if _scheduler is None:
        return
    _scheduler.shutdown(wait=False)
    _scheduler = None
    log.info("APScheduler stopped")
