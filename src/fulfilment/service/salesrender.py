from . import db
from ..facades.salesrender import SalesrenderFacade


def update_crm_statuses(crm_statuses_to_update: dict):
    for crm_id, orders in crm_statuses_to_update.items():
        crm_interface = db.get_leadvertex_api_by_crm_id(crm_id)
        salesrender_api = SalesrenderFacade(crm_interface.lv_api_token, crm_interface.lv_link, crm_interface.crm_id)
        response = salesrender_api.update_several_statuses_cs(orders)
        db.mark_ff_following_statuses_as_updated(orders.keys())
        return response