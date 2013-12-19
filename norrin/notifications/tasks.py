import datetime

# import urbanairship as ua
from celery import Celery
from celery.utils.log import get_task_logger

# import config
# from .services import BillService, BillActionService, VoteService, adapters
# from .adapters import UrbanAirshipAdapter

logger = get_task_logger(__name__)

celery = Celery()
celery.config_from_object('celeryconfig')

# airship = ua.Airship(config.UA_KEY, config.UA_MASTER)

# adapters.register(UrbanAirshipAdapter(airship))


@celery.task
def run_bill_service():
    logger.debug('running BillService!!!!!!!!')
#     BillService().run()


@celery.task
def run_bill_action_service():
    logger.debug('running BillActionService!!!!!!!!')
#     BillActionService().run()


@celery.task
def run_vote_service():
    logger.debug('running VoteService at!!!!!!!!')
#     VoteService().run()
