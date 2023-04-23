from django.urls import path, include

from accounts.views import RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register')
]
