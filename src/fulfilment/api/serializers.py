from rest_framework import serializers

from .. import models


class CRMDealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CRMDealItem
        fields = '__all__'


class CRMDealInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CRMDealInfo
        fields = '__all__'


class CRMInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CRMInterface
        fields = '__all__'


class CRMStatusIdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CRMStatusIds
        fields = '__all__'


class FulfillmentCRMConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FulfillmentCRMConnections
        fields = '__all__'


class FulfillmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fulfillment
        fields = '__all__'

class FulfillmentFollowingStatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FulfillmentFollowingStatuses
        fields = '__all__'
