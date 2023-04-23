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
from accounts.serializers import *


class RegisterUserView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = AddUserSerializer


class BaseUserViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = BaseUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['GET', ])
    def view_profile(self, request, pk=None):
        if not BaseUser.objects.filter(id=pk).exists():
            response = {'message': "user not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        user = BaseUser.objects.get(id=pk)
        if user.is_staff:
            response = {'message': "staff users do not have a profile"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(parent_base_user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
