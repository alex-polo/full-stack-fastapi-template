from logging import Formatter

from gunicorn.config import Config
from gunicorn.glogging import Logger

from ..config import SERVER_SETTINGS as SETTINGS


class GunicornLogger(Logger):  # type: ignore[misc]
    """Custom Gunicorn logger."""

    def setup(self, cfg: Config) -> None:
        """Setup Gunicorn logger."""
        super().setup(cfg)

        self._set_handler(  # type: ignore[unused-ignore]
            log=self.access_log,
            output=cfg.accesslog,
            fmt=Formatter(
                fmt=SETTINGS.LOGGING.log_format,
                datefmt=SETTINGS.LOGGING.log_date_format,
            ),
        )

        self._set_handler(  # type: ignore[unused-ignore]
            log=self.error_log,
            output=cfg.errorlog,
            fmt=Formatter(
                fmt=SETTINGS.LOGGING.log_format,
                datefmt=SETTINGS.LOGGING.log_date_format,
            ),
        )
