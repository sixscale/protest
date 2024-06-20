from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
import datetime

from .permissions import PermissionTokenIsCorrect, PermissionSlugIsMissing
from .serializers import FulfillmentCRMConnectionsSerializer
from ..service.webhook_handler import webhook_handler
from ..tasks import handle_webhook_task


class ProductCreationView(CreateAPIView):
    serializer_class = FulfillmentCRMConnectionsSerializer
    permission_classes = [PermissionTokenIsCorrect]


class ProtestCRMDealUpdateView(CreateAPIView):
    permission_classes = [PermissionSlugIsMissing]
    
    def post(self, request, *args, **kwargs):
        handle_webhook_task.delay(data=request.data, crm_title=kwargs.get('crm_title'))
        print(Response(status=status.HTTP_200_OK))
        return Response(status=status.HTTP_200_OK)
