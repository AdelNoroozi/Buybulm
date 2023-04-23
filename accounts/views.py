from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.models import *
from accounts.serializers import AddUserSerializer


class RegisterUserView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = AddUserSerializer
