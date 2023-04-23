from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import *

router = DefaultRouter()
router.register('users', BaseUserViewSet)
router.register('admins', AdminViewSet)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('add-admin/', AddAdminView.as_view(), name='add_admin'),
    path('', include(router.urls))
]
