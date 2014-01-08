import os
from celery.schedules import crontab

BROKER_URL = os.environ.get('CELERY_BROKER')

CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'vote_service': {
        'task': 'norrin.notifications.tasks.run_vote_service',
        'schedule': crontab(minute='*'), # every 14 minutes
    },
    'bill_service': {
        'task': 'norrin.notifications.tasks.run_bill_service',
        'schedule': crontab(hour='*', minute="0"), # every hour, on the hour
    },
    'bill_action_service': {
        'task': 'norrin.notifications.tasks.run_bill_action_service',
        'schedule': crontab(hour='*', minute="30"), # every hour, 30 minutes in
    },
    'upcoming_bill_service': {
        'task': 'norrin.notifications.tasks.run_upcoming_bill_service',
        'schedule': crontab(hour='*', minute="15"), # every hour, 30 minutes in
    },
}
