from datetime import datetime
import json
import logging

from .validation import CRMDealInfoValidator, CRMDealItemValidator
request_logger = logging.getLogger("ff_request")
response_logger = logging.getLogger("ff_response")
sync_logger = logging.getLogger("ff_sync")


def log_request(crm_title: str, request_data: dict, validated_deal: CRMDealInfoValidator, validated_deal_items: list[CRMDealItemValidator]):
    deal_items = "".join([f"\n\t{i + 1}: {item}" for i, item in enumerate(validated_deal_items)])
    request_logger.info(
        f"crm: {crm_title}\n"
        f"request time: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"request data: {json.dumps(request_data)}\n"
        f"deal: {validated_deal}\n"
        f"deal items: {deal_items}\n".encode('ascii', 'ignore').decode('ascii')
    )


def log_response(ff_response: dict, sr_response: dict):
    response_logger.info(
        f"response time: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"fulfilment response text: {json.dumps(ff_response)}\n"
        f"salesrender response text: {json.dumps(sr_response)}\n"
    )


def log_sync(ff_response: dict, sr_response: dict):
    sync_logger.info(
        f"response time: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"fulfilment response text: {json.dumps(ff_response)}\n"
        f"salesrender response text: {json.dumps(sr_response)}\n"
    )