import os
from celery import Celery



celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("REDISTOGO_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("REDISTOGO_URL", "redis://localhost:6379")


