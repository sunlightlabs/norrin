#!/bin/bash

celery worker -A norrin.notifications.tasks -l INFO -f celerybeat.stdout.log --beat
