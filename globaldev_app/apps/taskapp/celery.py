import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("globaldev_app")
# Using a string here means the worker doesn't have to serialize the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "collect_reading_time_statistic": {
        "task": "globaldev_app.apps.users.tasks.collect_reading_time_statistic",
        "schedule": crontab(minute="0", hour="0"),
    },
}

app.conf.timezone = "UTC"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # pragma: no cover
