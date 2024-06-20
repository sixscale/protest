from django.db import models


class CRMDealInfo(models.Model):
    # meta
    created_at_db = models.DateTimeField(auto_now_add=True)

    # crm
    crm_id = models.IntegerField()
    project_name = models.CharField(max_length=255)
    status_name = models.CharField(max_length=255)
    status_changed_at = models.DateTimeField()
    created_at_crm = models.DateTimeField()
    updated_at_crm = models.DateTimeField()

    # user
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    # operator
    support_operator_id = models.CharField(max_length=255)
    support_first_name = models.CharField(max_length=255)
    support_last_name = models.CharField(max_length=255)

    # address
    postcode = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    building = models.CharField(max_length=255, blank=True)
    apartment = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)

    # order
    order_confirmation_date = models.DateTimeField()
    substatus = models.CharField(max_length=255, blank=True)
    the_courier_was_polite = models.CharField(max_length=255, blank=True)
    was_the_client_at_the_address = models.CharField(max_length=255, blank=True)
    did_the_courier_arrive = models.CharField(max_length=255, blank=True)
    was_the_sms_from_courier = models.CharField(max_length=255, blank=True)
    original_order_id = models.CharField(max_length=255, blank=True)
    original_operator_order = models.CharField(max_length=255, blank=True)
    working_days = models.CharField(max_length=255, blank=True)
    comment_after_call = models.CharField(max_length=255, blank=True)
    original_delivery_status = models.CharField(max_length=255, blank=True)
    original_status_cs = models.CharField(max_length=255, blank=True)
    original_order_list = models.CharField(max_length=255, blank=True)
    customer_address = models.CharField(max_length=255, blank=True)
    original_track_number = models.CharField(max_length=255, blank=True)
    comment_for_cs = models.CharField(max_length=255, blank=True)
    delivery_status = models.CharField(max_length=255, blank=True)
    status_cs = models.CharField(max_length=255, blank=True)
    track_number = models.CharField(max_length=255, blank=True)
    original_comment_for_cs = models.CharField(max_length=255, blank=True)
    timezoneOffset = models.CharField(max_length=255, blank=True)
    exception = models.CharField(max_length=255, blank=True)
    cart_total_in_euros = models.FloatField()

    # reminder
    reminder_timer = models.DateTimeField()
    reminder_comment = models.CharField(max_length=255, blank=True)

    # source
    source_uri = models.CharField(max_length=255, blank=True)
    source_refererUri = models.CharField(max_length=255, blank=True)
    source_ip = models.CharField(max_length=255, blank=True)
    source_utm_source = models.CharField(max_length=255, blank=True)
    source_utm_medium = models.CharField(max_length=255, blank=True)
    source_utm_campaign = models.CharField(max_length=255, blank=True)
    source_utm_content = models.CharField(max_length=255, blank=True)
    source_utm_term = models.CharField(max_length=255, blank=True)
    source_subid_1 = models.CharField(max_length=255, blank=True)
    source_subid_2 = models.CharField(max_length=255, blank=True)


class CRMDealItem(models.Model):
    deal = models.ForeignKey(CRMDealInfo, related_name='Deal', on_delete=models.CASCADE)
    sku_title = models.CharField(max_length=255)
    sku_id = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price_in_euros = models.FloatField()


class FulfillmentCRMConnections(models.Model):
    banned_country = models.CharField(max_length=255)
    working_country = models.CharField(max_length=255)
    crm_title = models.CharField(max_length=255)
    crm_product_title = models.CharField(max_length=255)
    crm_product_id = models.CharField(max_length=255)
    ff_product_code = models.CharField(max_length=255)
    ff_login = models.CharField(max_length=255)


class Fulfillment(models.Model):
    title = models.CharField(max_length=255)
    inner_id = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    api_link = models.CharField(max_length=255)


class FulfillmentFollowingStatuses(models.Model):
    crm_id = models.IntegerField()
    ff_order_number = models.CharField(max_length=255)
    ff_id = models.CharField(max_length=255)
    ff_status = models.TextField(blank=True)
    is_status_updated_in_crm = models.BooleanField(default=True)


class CRMInterface(models.Model):
    crm_title = models.CharField(max_length=255, unique=True)
    crm_id = models.IntegerField()
    lv_api_token = models.CharField(max_length=350)
    lv_link = models.CharField(max_length=255)
    lv_prefix = models.CharField(max_length=255)


class CRMStatusIds(models.Model):
    crm_title = models.CharField(max_length=255)
    status_title = models.CharField(max_length=255)
    status_id = models.IntegerField()
