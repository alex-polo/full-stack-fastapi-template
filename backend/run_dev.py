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
    )


if __name__ == "__main__":
    main()
