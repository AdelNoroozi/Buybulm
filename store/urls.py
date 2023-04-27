from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store.views import *

router = DefaultRouter()
router.register('payments', PaymentViewSet)
urlpatterns = [
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('', include(router.urls))
]
