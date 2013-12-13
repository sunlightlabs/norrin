import os
from celery.schedules import crontab


BROKER_URL = os.environ.get('CELERY_BROKER')
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'every-15-minutes': {
        'task': 'norrin.notifications.run_vote_service',
        'schedule': crontab(minute='*/15'),
    },
    'every-minute-at-3pm': {
        'task': 'norrin.notifications.run_bill_service',
        'schedule': crontab(hour='21'), # UTC hour
    },
}
