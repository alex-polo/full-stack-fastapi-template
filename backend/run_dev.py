import uvicorn

from src.core.config import APP_SETTINGS
from src.core.config.logging import setup_logging


def main() -> None:
    """Main function."""
    setup_logging()

    uvicorn.run(
        "src.main:app",
        host=APP_SETTINGS.UVICORN.host,
        port=APP_SETTINGS.UVICORN.port,
        reload=APP_SETTINGS.UVICORN.reload,
        loop=APP_SETTINGS.UVICORN.loop,
        http=APP_SETTINGS.UVICORN.http,
        lifespan=APP_SETTINGS.UVICORN.lifespan,
        access_log=APP_SETTINGS.UVICORN.access_log,
        use_colors=APP_SETTINGS.UVICORN.use_colors,
    )


if __name__ == "__main__":
    main()
