import logging

from celery import shared_task

log = logging.getLogger(__name__)


@shared_task(name="src.notifications.tasks.test_task")
def test_task(message: str) -> str:
    """Test task."""
    log.info("Test task, received message: %s", message)
    return f"Test task: {message}"
