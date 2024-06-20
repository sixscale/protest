# tasks.py
from celery import shared_task
from .service.webhook_handler import webhook_handler

@shared_task
def handle_webhook_task(data, crm_title):
    return webhook_handler(data, crm_title)
