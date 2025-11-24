from src.core.config import SERVER_SETTINGS as SETTINGS
from src.core.gunicorn import GunicornApplication
from src.core.gunicorn.application import get_gunicorn_options
from src.main import app as main_app


def main() -> None:
    """Starting FastAPI-application in production mode with Gunicorn."""
    options: dict[str, str] = get_gunicorn_options(
        host=SETTINGS.GUNICORN.host,
        port=SETTINGS.GUNICORN.port,
        timeout=SETTINGS.GUNICORN.timeout,
        workers=SETTINGS.GUNICORN.workers,
        worker_class=SETTINGS.GUNICORN.worker_class,
        log_level=SETTINGS.GUNICORN.log_level,
        access_log=SETTINGS.GUNICORN.access_log,
        error_log=SETTINGS.GUNICORN.error_log,
    )

    GunicornApplication(app=main_app, options=options).run()
