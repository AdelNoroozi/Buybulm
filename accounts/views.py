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

    @classmethod
    def get_user_by_id(cls, _id):
        if BaseUser.objects.filter(id=_id).exists():
            return BaseUser.objects.get(id=_id)

    @action(detail=True, methods=['GET', ])
    def view_profile(self, request, pk=None):
        user = BaseUserViewSet.get_user_by_id(_id=pk)
        if not user:
            response = {'message': "user not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        if user.is_staff:
            response = {'message': "staff users do not have a profile"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(parent_base_user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH', ])
    def activate_account(self, request, pk=None):
        user = BaseUserViewSet.get_user_by_id(_id=pk)
        if not user:
            response = {'message': "user not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        if user.is_superuser:
            response = {'message': 'can not perform this action on superuser'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if user.is_active:
            response = {'message': 'account is already active.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        response = {'message': 'account activated successfully.'}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH', ])
    def deactivate_account(self, request, pk=None):
        user = BaseUserViewSet.get_user_by_id(_id=pk)
        if not user:
            response = {'message': "user not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        if user.is_superuser:
            response = {'message': 'can not perform this action on superuser'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            response = {'message': 'account is already deactivated.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        response = {'message': 'account deactivated successfully.'}
        return Response(response, status=status.HTTP_200_OK)


class AddAdminView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = AddAdminSerializer
# class AdminViewSet(mixins.ListModelMixin,
#                    mixins.RetrieveModelMixin,
#                     )
