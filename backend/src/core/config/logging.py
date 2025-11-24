import logging

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .constants import SERVER_SETTINGS as SETTINGS


def setup_logging() -> None:
    """Apply logging configuration from settings."""
    if SETTINGS.LOGGING.sentry_dsn and SETTINGS.ENVIRONMENT != "local":
        sentry_sdk.init(
            dsn=str(SETTINGS.LOGGING.sentry_dsn),
            environment=SETTINGS.ENVIRONMENT,
            traces_sample_rate=SETTINGS.LOGGING.sentry_traces_sample_rate,
            enable_tracing=True,
            integrations=[
                FastApiIntegration(),
                LoggingIntegration(
                    level=logging.INFO,
                    event_level=getattr(
                        logging, SETTINGS.LOGGING.sentry_log_level
                    ),
                ),
            ],
        )

    logging.basicConfig(
        level=SETTINGS.LOGGING.log_level,
        format=SETTINGS.LOGGING.log_format,
        datefmt=SETTINGS.LOGGING.log_date_format,
        force=True,
    )
