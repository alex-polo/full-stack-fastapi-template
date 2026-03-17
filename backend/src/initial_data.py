import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def init() -> None:
    """Initialize database connection."""
    ...


def main() -> None:
    """Run before the server starts."""
    log.info("Creating initial data")
    init()
    log.info("Initial data created")


if __name__ == "__main__":
    main()
