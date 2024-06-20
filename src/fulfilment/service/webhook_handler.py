from . import db
from pydantic import ValidationError
from .logger import log_request, log_response
from ..facades.fulfilment import FulfilmentAPI
from ..facades.salesrender import SalesrenderFacade
from .fulfilment import get_ff_creating_order_request_body
from .validation import (
    CRMDealInfoValidator,
    CRMDealItemValidator,
    FulfillmentFollowingStatusesValidator,
)


def webhook_handler(request_data: dict, crm_title: str) -> None:
    crm_interface = db.get_leadvertex_api_by_title(crm_title)
    validated_deal = get_validated_deal(request_data, crm_title, crm_interface.lv_prefix)
    validated_deal_items = get_validated_deal_items(request_data)
    log_request(crm_title, request_data, validated_deal, validated_deal_items)
    db.save_deal(validated_deal, validated_deal_items)
    ff_response = send_items_to_fulfilment(validated_deal, validated_deal_items, crm_interface.crm_id)
    salesrender_api = SalesrenderFacade(crm_interface.lv_api_token, crm_interface.lv_link, crm_interface.crm_id)
    if is_successful_ff_response(ff_response):
        exported_status_id = db.get_exported_status_id(crm_title)
        sr_response = salesrender_api.update_status(validated_deal.crm_id, exported_status_id)
    else:
        error = ff_response.get('errors')[0].get('description')
        sr_response = salesrender_api.update_status_cs(validated_deal.crm_id, error)
    log_response(ff_response, sr_response)


def is_successful_ff_response(ff_response: dict) -> bool:
    return "errors" not in ff_response


def get_validated_deal(request_data: dict, crm_title: str, crm_prefix: str) -> CRMDealInfoValidator:
    validated_deal = CRMDealInfoValidator.model_validate(request_data)
    validated_deal.crm_title = crm_title
    validated_deal.order_number = f"{crm_prefix}{validated_deal.crm_id}"
    return validated_deal


def get_validated_deal_items(request_data: dict) -> list[CRMDealItemValidator]:
    items = []
    promotions = request_data.get("cart", {}).get("promotions", [])
    for promotion in promotions:
        for item in promotion.get("items", []):
            items.append(CRMDealItemValidator.model_validate(item))
    return items


def send_items_to_fulfilment(
        validated_deal: CRMDealInfoValidator,
        validated_deal_items: list[CRMDealItemValidator],
        crm_id: int,
) -> dict:
    ff_connection = db.get_fulfilment_to_product_connection(validated_deal, validated_deal_items[0])
    ff_creds = db.get_fulfilment(ff_connection)
    ff_api = FulfilmentAPI(login=ff_creds.login, password=ff_creds.password, api_link=ff_creds.api_link)
    ff_request_body = get_ff_creating_order_request_body(
        deal=validated_deal,
        validated_deal_items=validated_deal_items,
        ff_connection=ff_connection,
        ff_creds=ff_creds
    )
    response = ff_api.create_order(ff_request_body).json()
    status = FulfillmentFollowingStatusesValidator(
        crm_id=crm_id,
        ff_order_number=validated_deal.order_number,
        ff_id=ff_creds.inner_id,
        ff_status=""
    )
    db.add_status_to_following(status)
    return response
