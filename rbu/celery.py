# https://www.codingforentrepreneurs.com/blog/celery-redis-django/
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rbu.settings')

app = Celery('rbu')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
app.conf.beat_schedule = {

    'add-every-5-seconds': {
        'task': 'task_import_csv',
        'schedule': 15.0
    },

}

# for debug
# celery -A rbu worker -B -l info

# for production
# celery -A rbu worker -l info
# celery -A rbu beat -l info
# redis-server


