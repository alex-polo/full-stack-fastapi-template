from celery import Celery

from src.core.config import init_celery_sentry

init_celery_sentry()

celery_app = Celery("worker")

celery_app.config_from_object("src.core.config.celeryconfig")

celery_app.autodiscover_tasks(["src.modules"])
