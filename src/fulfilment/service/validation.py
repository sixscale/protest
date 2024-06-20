from datetime import datetime

from pydantic import (
    BaseModel,
    field_validator,
    Field,
    AliasPath,
    EmailStr,
    validator,
    computed_field
)


class CRMDealInfoValidator(BaseModel):
    # crm
    crm_id: int = Field(validation_alias=AliasPath("id"), default=0)
    crm_title: str =  Field(default="")
    project_name: str = Field(validation_alias=AliasPath("project", "name"), default="")
    status_name: str = Field(validation_alias=AliasPath("status", "name"), default="")
    status_changed_at: datetime = Field(validation_alias=AliasPath("statusChangedAt"), default="")
    created_at_crm: datetime = Field(validation_alias=AliasPath("createdAt"), default="")
    updated_at_crm: datetime = Field(validation_alias=AliasPath("updatedAt"), default="")

    # user
    email: str = Field(validation_alias=AliasPath("data", "emailFields", 0, "value", "raw"), default="")
    first_name: str = Field(validation_alias=AliasPath("data", "humanNameFields", 0, "value", "firstName"), default="")
    second_name: str = Field(validation_alias=AliasPath("data", "humanNameFields", 0, "value", "lastName"), default="")
    # country относится к адресу, сюда пришлось перенести, для корректной валидации номера
    country: str = Field(validation_alias=AliasPath("data", "addressFields", 0, "value", "country"), default="")
    phone: str = Field(validation_alias=AliasPath("data", "phoneFields", 0, "value", "phone", "international"), default="")

    # operator
    support_operator_id: str = Field(validation_alias=AliasPath("data", "userFields", 0, "value", "id"), default="")
    support_first_name: str = Field(validation_alias=AliasPath("data", "userFields", 0, "value", "name", "firstName"), default="")
    support_last_name: str = Field(validation_alias=AliasPath("data", "userFields", 0, "value", "name", "lastName"), default="")

    # address
    postcode: str = Field(validation_alias=AliasPath("data", "addressFields", 0, "value", "postcode"), default="")
    region: str = Field(validation_alias=AliasPath("data", "addressFields", 0, "value", "region"), default="")
    city: str = Field(validation_alias=AliasPath("data", "addressFields", 0, "value", "city"), default="")
    address_1: str = Field(validation_alias=AliasPath("data", "addressFields", 0, "value", "address_1"), default="")
    address_2: str = Field(validation_alias=AliasPath("data", "addressFields", 0, "value", "address_2"), default="")
    building: str = Field(validation_alias=AliasPath("data", "addressFields", 0, "value", "building"), default="")
    apartment: str = Field(validation_alias=AliasPath("data", "addressFields", 0, "value", "apartment"), default="")

    # order
    order_number: str = Field(default="")
    order_confirmation_date: datetime = Field(validation_alias=AliasPath("data", "dateTimeFields", 0, "value"), default="")
    substatus: str = Field(validation_alias=AliasPath("data", "enumFields", 0, "value"), default="")
    the_courier_was_polite: str = Field(validation_alias=AliasPath("data", "enumFields", 1, "value"), default="")
    was_the_client_at_the_address: str = Field(validation_alias=AliasPath("data", "enumFields", 2, "value"), default="")
    did_the_courier_arrive: str = Field(validation_alias=AliasPath("data", "enumFields", 3, "value"), default="")
    was_the_sms_from_courier: str = Field(validation_alias=AliasPath("data", "enumFields", 4, "value"), default="")
    original_order_id: str = Field(validation_alias=AliasPath("data", "stringFields", 0, "value"), default="")
    original_operator_order: str = Field(validation_alias=AliasPath("data", "stringFields", 1, "value"), default="")
    working_days: str = Field(validation_alias=AliasPath("data", "stringFields", 2, "value"), default="")
    comment_after_call: str = Field(validation_alias=AliasPath("data", "stringFields", 3, "value"), default="")
    original_delivery_status: str = Field(validation_alias=AliasPath("data", "stringFields", 4, "value"), default="")
    original_status_cs: str = Field(validation_alias=AliasPath("data", "stringFields", 5, "value"), default="")
    original_order_list: str = Field(validation_alias=AliasPath("data", "stringFields", 6, "value"), default="")
    customer_address: str = Field(validation_alias=AliasPath("data", "stringFields", 7, "value"), default="")
    original_track_number: str = Field(validation_alias=AliasPath("data", "stringFields", 8, "value"), default="")
    comment_for_cs: str = Field(validation_alias=AliasPath("data", "stringFields", 9, "value"), default="")
    delivery_status: str = Field(validation_alias=AliasPath("data", "stringFields", 10, "value"), default="")
    status_cs: str = Field(validation_alias=AliasPath("data", "stringFields", 11, "value"), default="")
    track_number: str = Field(validation_alias=AliasPath("data", "stringFields", 12, "value"), default="")
    original_comment_for_cs: str = Field(validation_alias=AliasPath("data", "stringFields", 13, "value"), default="")
    timezoneOffset: str = Field(validation_alias=AliasPath("timezoneOffset"), default="")
    exception: str  = Field(validation_alias=AliasPath("exception"), default="")
    cart_total_in_cents: int = Field(validation_alias=AliasPath("cart", "promotions", 0, "total"), default=0)

    # reminder
    reminder_timer: str = Field(validation_alias=AliasPath("reminder", "timer"), default="")
    reminder_comment: str = Field(validation_alias=AliasPath("reminder", "comment"), default="")

    # source
    source_uri: str = Field(validation_alias=AliasPath("source", "uri"), default="")
    source_refererUri: str = Field(validation_alias=AliasPath("source", "refererUri"), default="")
    source_ip: str = Field(validation_alias=AliasPath("source", "ip"), default="")
    source_utm_source: str = Field(validation_alias=AliasPath("source", "utm_source"), default="")
    source_utm_medium: str = Field(validation_alias=AliasPath("source", "utm_medium"), default="")
    source_utm_campaign: str = Field(validation_alias=AliasPath("source", "utm_campaign"), default="")
    source_utm_content: str = Field(validation_alias=AliasPath("source", "utm_content"), default="")
    source_utm_term: str = Field(validation_alias=AliasPath("source", "utm_term"), default="")
    source_subid_1: str = Field(validation_alias=AliasPath("source", "subid_1"), default="")
    source_subid_2: str = Field(validation_alias=AliasPath("source", "subid_2"), default="")

    @computed_field
    @property
    def cart_total_in_euros(self) -> float:
        return self.cart_total_in_cents / 100

    @validator('*', pre=True, always=True)
    def replace_none_with_empty_str(cls, v):
        if v is None:
            return ""
        return v
    
    @validator('phone', pre=True, always=True)
    def cut_the_phone_number(cls, v, values):
        country_value = values.get('country')
        if country_value == 'ES':
            return v[3:]
        elif country_value == 'PT':
            return v[4:]
        else:
            return v


class CRMDealItemValidator(BaseModel):
    sku_title: str = Field(validation_alias=AliasPath("sku", "item", "name"), default="")
    sku_id: str = Field(validation_alias=AliasPath("sku", "item", "id"), default="")
    price_in_cents: int = Field(validation_alias=AliasPath("price"), default=0)
    quantity: int = Field(default=1)

    @computed_field
    @property
    def price_in_euros(self) -> float:
        return self.price_in_cents / 100


class CRMInterfaceValidation(BaseModel):
    crm_title: str = Field(default="")
    crm_id: int = Field(default=0)
    lv_api_token: str = Field(default="")
    lv_link: str = Field(default="")
    lv_prefix: str = Field(default="")


class FulfillmentCRMConnectionsValidator(BaseModel):
    banned_country: str
    working_country: str
    crm_title: str
    crm_product_title: str
    crm_product_id: str
    ff_product_code: str
    ff_login: str


class FulfilmentValidator(BaseModel):
    inner_id: str
    title: str
    login: str
    password: str
    api_link: str


class FulfillmentFollowingStatusesValidator(BaseModel):
    crm_id: int
    ff_order_number: str
    ff_id: str
    ff_status: str
    is_status_updated_in_crm: bool = Field(default=False)
