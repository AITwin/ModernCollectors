import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ModernCollectors.settings")

app = Celery("celert-collectors")

app.conf.broker_url = "redis://localhost:6379/0"

app.config_from_object("django.conf:settings", namespace="COLLECTORS")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
