from django.urls import path

from .views import (
    ProtestCRMDealUpdateView,
    ProductCreationView,
)


urlpatterns = [
    path('crm/<str:crm_title>/', ProtestCRMDealUpdateView.as_view()),
    path('create-product/', ProductCreationView.as_view()),
]
