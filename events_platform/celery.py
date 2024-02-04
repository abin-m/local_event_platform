from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_platform.settings')

# Create a Celery application
celery_app = Celery('events_platform')

# Load task modules from all registered Django app configs
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
