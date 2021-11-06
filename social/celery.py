import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')

app = Celery('social')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-post-every-5-minutes': {
        'task': 'network.tasks.send_posts',
        'schedule': crontab(minute='*/5'),
    },
}
