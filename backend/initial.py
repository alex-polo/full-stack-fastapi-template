import asyncio
import logging

from src.auth.application.init import init_admin

log = logging.getLogger(__name__)


async def initial_data() -> None:
    """Run before the uvicorn server starts."""
    log.info("pre_start")
    await init_admin()
    log.info("pre_start completed")


if __name__ == "__main__":
    asyncio.run(initial_data())
