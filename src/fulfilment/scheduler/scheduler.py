from apscheduler.schedulers.background import BackgroundScheduler

from ..service.fulfilment import sync_ff_and_crm_statuses


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_ff_and_crm_statuses, 'interval', minutes=20)
    scheduler.start()
