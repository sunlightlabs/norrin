#!/bin/bash

# celery worker -A norrin.notifications.tasks -l INFO -f celerybeat.stdout.log --beat

python -c "from norrin.notifications import tasks; tasks.run_bill_service()"
python -c "from norrin.notifications import tasks; tasks.run_bill_action_service()"
python -c "from norrin.notifications import tasks; tasks.run_upcoming_bill_service()"
python -c "from norrin.notifications import tasks; tasks.run_vote_service()"
