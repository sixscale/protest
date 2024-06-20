from . import exceptions
from . import validation
from ..api import serializers
from .. import models


#leadvertex
def save_deal(validated_deal: validation.CRMDealInfoValidator, validated_deal_items: list[validation.CRMDealItemValidator]) -> int:
    serializer = serializers.CRMDealInfoSerializer(data=validated_deal.dict())
    if not serializer.is_valid():
        return -1
    serializer.save()
    deal_id = serializer.data.get("id")
    for item in validated_deal_items:
        data = item.dict()
        data["deal"] = deal_id
        serializer_item = serializers.CRMDealItemSerializer(data=data)
        if not serializer_item.is_valid():
            return -1
        serializer_item.save()
    return deal_id

def get_leadvertex_api_by_title(crm_title: str) -> validation.CRMInterfaceValidation:
    try:
        leadvertex_api = models.CRMInterface.objects.get(crm_title=crm_title)
    except models.CRMInterface.DoesNotExist:
        raise exceptions.LeadvertexAPIDoesNotExist(f"Not found api for crm {crm_title}")
    leadvertex_api_serializer = serializers.CRMInterfaceSerializer(leadvertex_api).data
    return validation.CRMInterfaceValidation.model_validate(leadvertex_api_serializer)


def get_exported_status_id(crm_title: str):
    try:
        status_by_title = models.CRMStatusIds.objects.get(crm_title=crm_title, status_title="Exported")
    except models.CRMStatusIds.DoesNotExist:
        raise exceptions.LeadvertexExportedStatusNotFound(f"Not found 'Exported' status in crm {crm_title}")
    status_id_serializer = serializers.CRMStatusIdsSerializer(status_by_title).data
    return status_id_serializer.get("status_id", "")


def add_status_to_following(status: validation.FulfillmentFollowingStatusesValidator):
    serializer = serializers.FulfillmentFollowingStatusesSerializer(data=status.dict())
    serializer.is_valid(raise_exception=True)
    serializer.save()


def get_leadvertex_api_by_crm_id(crm_id: int) -> validation.CRMInterfaceValidation:
    try:
        leadvertex_api = models.CRMInterface.objects.get(crm_id=crm_id)
    except models.CRMInterface.DoesNotExist:
        raise exceptions.LeadvertexAPIDoesNotExist(f"Not found api for crm {crm_id}")
    leadvertex_api_serializer = serializers.CRMInterfaceSerializer(leadvertex_api).data
    return validation.CRMInterfaceValidation.model_validate(leadvertex_api_serializer)


# fulfilment
def get_fulfilment_to_product_connection(
        validated_deal: validation.CRMDealInfoValidator,
        product: validation.CRMDealItemValidator
) -> validation.FulfillmentCRMConnectionsValidator:
    product_filter = models.FulfillmentCRMConnections.objects.filter(
        crm_title=validated_deal.crm_title,
        crm_product_id=product.sku_id
    )
    if not product_filter.exists():
        raise exceptions.FulfilmentNotFoundException(
            f"Not found fulfilment.\n"
            f"CRM Product id: {product.sku_id}\n"
            f"CRM: {validated_deal.crm_title}\n"
        )
    if validated_deal.country != "BG":
        fulfillment_crm_connection = product_filter.get(banned_country="BG")
    else:
        fulfillment_crm_connection = product_filter.get(working_country="BG")
    return validation.FulfillmentCRMConnectionsValidator.model_validate(
        serializers.FulfillmentCRMConnectionsSerializer(fulfillment_crm_connection).data
    )


def get_fulfilment(
        fulfillment_crm_connection: validation.FulfillmentCRMConnectionsValidator
) -> validation.FulfilmentValidator:
    if not models.Fulfillment.objects.filter(login=fulfillment_crm_connection.ff_login).exists():
        raise exceptions.FulfilmentCredentialsNotFoundException(
            f"Not found fulfilment credentials.\n"
            f"Fulfilment login: {fulfillment_crm_connection.ff_login}\n"
        )
    fulfilment_serializer = serializers.FulfillmentSerializer(
        models.Fulfillment.objects.get(login=fulfillment_crm_connection.ff_login)
    ).data
    return validation.FulfilmentValidator.model_validate(fulfilment_serializer)


def get_all_ffs() -> list[validation.FulfilmentValidator]:
    fulfilment_serializer = serializers.FulfillmentSerializer(models.Fulfillment.objects.all(), many=True).data
    return [validation.FulfilmentValidator.model_validate(ff) for ff in fulfilment_serializer]


def get_following_orders_by_ff(ff_id: str) -> list[validation.FulfillmentFollowingStatusesValidator]:
    ff_statuses_serializer = serializers.FulfillmentFollowingStatusesSerializer(
        models.FulfillmentFollowingStatuses.objects.filter(ff_id=ff_id), many=True
    ).data
    return [status.get("ff_order_number") for status in ff_statuses_serializer]


def get_ff_following_statuses_by_order_number(order_number: str) -> validation.FulfillmentFollowingStatusesValidator:
    try:
        ff_following_status_serializer = serializers.FulfillmentFollowingStatusesSerializer(
            models.FulfillmentFollowingStatuses.objects.get(ff_order_number=order_number)
        ).data
        return validation.FulfillmentFollowingStatusesValidator.model_validate(ff_following_status_serializer)
    except models.FulfillmentFollowingStatuses.DoesNotExist:
        raise exceptions.FollowingOrderNotFoundException(f"Not found order with number {order_number}")


def update_ff_following_status(order_number: str, order_status_cs: str) -> None:
    models.FulfillmentFollowingStatuses.objects.filter(ff_order_number=order_number).update(
        ff_status=order_status_cs,
        is_status_updated_in_crm=False,
    )


def mark_ff_following_statuses_as_updated(order_numbers: dict) -> None:
    for order_number in order_numbers:
        models.FulfillmentFollowingStatuses.objects.filter(ff_order_number=order_number).update(
            is_status_updated_in_crm=True,
        )
