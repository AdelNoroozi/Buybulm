from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import CreatePaymentView

urlpatterns = [
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment')
]
