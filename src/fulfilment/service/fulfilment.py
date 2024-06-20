from datetime import datetime

from . import db
from . import validation
from ..facades.fulfilment import FulfilmentAPI
from .salesrender import update_crm_statuses
from .logger import log_sync


def get_ff_creating_order_request_body(
        deal: validation.CRMDealInfoValidator,
        validated_deal_items: list[validation.CRMDealItemValidator],
        ff_connection: validation.FulfillmentCRMConnectionsValidator,
        ff_creds: validation.FulfilmentValidator
) -> dict:
    items = [
        {
            "ItemCode": ff_connection.ff_product_code,
            "Quantity": item.quantity,
            "Price": item.price_in_euros
        }
        for item in validated_deal_items
    ]
    return {
            "OrderNumber": deal.order_number,
            "OrderDate": datetime.today().strftime('%Y-%m-%d'),
            "Name": deal.first_name,
            "Surname": deal.second_name,
            "MiddleName": "",
            "Email": deal.email,
            "PostalCode": deal.postcode,
            "Country": deal.country,
            "Region": deal.region,
            "City": deal.city,
            "District": "",
            "AppartmentNumber": "",
            "Street": deal.address_1,
            "BuildingNumber": deal.address_2,
            "Phone": deal.phone,
            "WarehouseID": ff_creds.inner_id,
            "Comments": deal.comment_for_cs,
            "CodAmount": deal.cart_total_in_euros,
            "items": items
        }


def sync_ff_and_crm_statuses():
    order_statuses = get_ff_order_statuses()
    crm_statuses_to_update = {}
    for order_number, order_status_cs in order_statuses.items():
        ff_following_status = db.get_ff_following_statuses_by_order_number(order_number)
        if ff_following_status.is_status_updated_in_crm and ff_following_status.ff_status == order_status_cs:
            continue
        if ff_following_status.ff_status != order_status_cs:
            db.update_ff_following_status(order_number, order_status_cs)
        if ff_following_status.crm_id not in crm_statuses_to_update:
            crm_statuses_to_update[ff_following_status.crm_id] = {}
        crm_statuses_to_update[ff_following_status.crm_id][order_number] = order_status_cs
    sr_response = update_crm_statuses(crm_statuses_to_update)
    log_sync(order_statuses, sr_response)


def get_ff_order_statuses():
    ffs = db.get_all_ffs()
    order_statuses = {}
    for ff_creds in ffs:
        following_orders = db.get_following_orders_by_ff(ff_id=ff_creds.inner_id)
        ff_api = FulfilmentAPI(login=ff_creds.login, password=ff_creds.password, api_link=ff_creds.api_link)
        ff_following_orders_statuses = ff_api.get_order_status({"OrderNumber": following_orders}).json()
        for order in ff_following_orders_statuses:
            status = order.get("Statuses")[-1]
            order_statuses[order.get("OrderNumber")] = f'{status.get("OrderStatus")} ({status.get("StatusCause")})'
    return order_statuses
