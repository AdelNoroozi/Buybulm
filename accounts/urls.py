from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('users', BaseUserViewSet)
router.register('admins', AdminViewSet)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('add-admin/', AddAdminView.as_view(), name='add_admin'),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('token/refresh/', TokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('whoami/', GetProfileView.as_view(), name='get_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('change_profile_info/', ChangeProfileInfoView.as_view(), name='change_profile_info'),
]
