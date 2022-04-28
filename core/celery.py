from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.conf.enable_utc = False

app.conf.update(timezone = 'Africa/Nairobi')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'test-celery-9': {
        'task': 'finance.task.test_celery',
        'schedule': crontab(hour=18, minute=46),
        # 'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
     
    }
    # 'send-mail-every-day-at-8': {
    #     'task': 'send_mail_app.tasks.send_mail_func',
    #     'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
     
    # }
    
}

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')