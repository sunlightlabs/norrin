import logging
from notifications.services import BillService, VoteService


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # BillService().run()
    VoteService().run()
