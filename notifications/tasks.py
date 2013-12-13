import datetime
import logging

from celery import Celery

# from .services import BillService, BillActionService, VoteService

logger = logging.getLogger('norrin.notifications')

celery = Celery('norrin.notifications')
celery.config_from_object('celeryconfig')


@celery.task
def run_bill_service():
    logger.info('running BillService at %s' % datetime.datetime.utcnow())
    # BillService().run()


@celery.task
def run_bill_action_service():
    logger.info('running BillActionService at %s' % datetime.datetime.utcnow())
    # BillActionService().run()


@celery.task
def run_vote_service():
    logger.info('running VoteService at %s' % datetime.datetime.utcnow())
    # VoteService().run()
