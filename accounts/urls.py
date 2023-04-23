from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import *

router = DefaultRouter()
router.register('users', BaseUserViewSet)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('', include(router.urls))
]
