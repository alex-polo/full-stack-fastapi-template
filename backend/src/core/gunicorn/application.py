from fastapi import FastAPI
from gunicorn.app.base import Application


class GunicornApplication(Application):  # type: ignore[misc]
    """Custom Gunicorn application for running a FastAPI."""

    def __init__(self, app: FastAPI, options: dict[str, str]) -> None:
        """Initialize Gunicorn application."""
        self.options: dict[str, str] = options
        self.application: FastAPI = app
        super().__init__()

    @property
    def config_options(self) -> dict[str, str]:
        """Get Gunicorn configuration options."""
        return {
            key: value
            for key, value in self.options.items()
            if key.lower() in self.cfg.settings and value is not None
        }

    def load_config(self) -> dict[str, str]:
        """Load Gunicorn configuration from the options."""
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)

        return self.options

    def load(self) -> FastAPI:
        """Return the FastAPI application instance to be served.

        This method is called by Gunicorn during startup.

        Returns:
            The FastAPI app instance.
        """
        return self.application


def get_gunicorn_options(
    host: str,
    port: int,
    timeout: int,
    workers: int,
    worker_class: str,
    log_level: str,
    access_log: str,
    error_log: str,
) -> dict[str, str]:
    """Get Gunicorn application options."""
    return {
        "bind": f"{host}:{port}",
        "timeout": str(timeout),
        "worker_class": worker_class,
        "workers": str(workers),
        "loglevel": log_level,
        "access_log": access_log,
        "error_log": error_log,
        "logger_class": "src.core.gunicorn.logger.GunicornLogger",
    }
