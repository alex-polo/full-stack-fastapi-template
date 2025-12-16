import asyncio
import contextlib
import logging
from typing import Final

from sqlalchemy import select
from tenacity import (
    before_log,
    before_sleep_log,
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)

from src.core.config.logging import setup_logging
from src.core.database.db_manager import DB_MANAGER

setup_logging()

log = logging.getLogger(__name__)

MAX_RETRIES: Final[int] = 60
WAIT_SECONDS: Final[int] = 5
AFTER_DELAY: Final[int] = 300  # 5 minutes


@retry(
    stop=(stop_after_attempt(MAX_RETRIES) | stop_after_delay(AFTER_DELAY)),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(log, logging.INFO),
    before_sleep=before_sleep_log(log, logging.WARNING),
)
async def await_db() -> None:
    """Run before the uvicorn server starts."""
    db_session_context = contextlib.asynccontextmanager(DB_MANAGER.get_session)
    async with db_session_context() as session:
        await session.execute(select(1))
    log.info("Database started")


if __name__ == "__main__":
    log.info("Await starting database")
    asyncio.run(await_db())
