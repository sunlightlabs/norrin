import datetime
import logging

import urbanairship as ua
from celery import Celery
from celery.utils.log import get_task_logger

from . import config
from .adapters import UrbanAirshipAdapter, ConsoleAdapter, LoggingAdapter, MongoDBAdapter
from .models import connection
from .services import BillService, BillActionService, UpcomingBillService, VoteService, adapters

logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)

celery = Celery('norrin.notifications.tasks')
celery.config_from_object('celeryconfig')

airship = ua.Airship(config.UA_KEY, config.UA_MASTER)

adapters.register(UrbanAirshipAdapter(airship))
adapters.register(MongoDBAdapter(connection[config.MONGODB_DATABASE]))
adapters.register(LoggingAdapter)


def nowstr():
    return datetime.datetime.utcnow().isoformat()

@celery.task
def run_bill_service():
    logger.info('running BillService at %s' % nowstr())
    BillService().run()


@celery.task
def run_bill_action_service():
    logger.info('running BillActionService at %s' % nowstr())
    BillActionService().run()


@celery.task
def run_upcoming_bill_service():
    logger.info('running UpcomingBillService at %s' % nowstr())
    UpcomingBillService().run()


@celery.task
def run_vote_service():
    logger.info('running VoteService at %s' % nowstr())
    VoteService().run()
