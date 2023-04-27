import re

from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.models import *
from accounts.permissions import *
from accounts.serializers import *


class RegisterUserView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = AddUserSerializer
    permission_classes = (NotAuthenticated,)


class BaseUserViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsUserAdmin,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BaseUser.objects.all()
        elif self.request.user.is_staff:
            return BaseUser.objects.filter(is_staff=False)
        else:
            return BaseUser.objects.none()

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
    def change_activation_status(self, request, pk=None):
        user = BaseUserViewSet.get_user_by_id(_id=pk)
        if not user:
            response = {'message': "user not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        if user.is_superuser:
            response = {'message': 'can not perform this action on superuser'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        if user.is_staff and (not request.user.is_superuser):
            response = {'message': 'only superusers can change staff users status'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        if user.is_active:
            user.is_active = False
            user.save()
            response = {'message': 'account deactivated successfully.'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            user.is_active = True
            user.save()
            response = {'message': 'account activated successfully.'}
            return Response(response, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['PATCH', ])
    # def deactivate_account(self, request, pk=None):
    #     user = BaseUserViewSet.get_user_by_id(_id=pk)
    #     if not user:
    #         response = {'message': "user not found"}
    #         return Response(response, status=status.HTTP_404_NOT_FOUND)
    #     if user.is_superuser:
    #         response = {'message': 'can not perform this action on superuser'}
    #         return Response(response, status=status.HTTP_400_BAD_REQUEST)
    #     if not user.is_active:
    #         response = {'message': 'account is already deactivated.'}
    #         return Response(response, status=status.HTTP_400_BAD_REQUEST)
    #     user.is_active = False
    #     user.save()
    #     response = {'message': 'account deactivated successfully.'}
    #     return Response(response, status=status.HTTP_200_OK)


class AddAdminView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = AddAdminSerializer
    permission_classes = (IsSuperUser,)


class AdminViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    @action(detail=True, methods=['PATCH', ])
    def set_section(self, request, pk=None):
        if not Admin.objects.filter(id=pk).exists():
            response = {'message': 'admin not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        try:
            section = request.data['section']
        except:
            response = {'message': 'field error: section'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if not (section == 'B' or section == 'S' or section == 'U'):
            response = {'message': 'invalid section'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        admin = Admin.objects.get(id=pk)
        admin.section = section
        admin.save()
        serializer = AdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class GetProfileView(APIView):
    permission_classes = (IsAuthenticatedAndNormalUser,)

    def get(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed('not authenticated')
        user = request.user
        if user.is_staff:
            response = {'message': 'staff users do not have a profile'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(parent_base_user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed('not authenticated')
        user = request.user
        try:
            current_password = request.data['current_password']
            new_password = request.data['new_password']
        except Exception as e:
            response = {'message': f'field error {str(e)}'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(current_password):
            response = {'message': 'incorrect password.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if current_password == new_password:
            response = {'message': 'new password can not be the same as current password.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user.password = make_password(new_password)
        user.save()
        response = {'message': 'password changed successfully.'}
        return Response(response, status=status.HTTP_202_ACCEPTED)


class ChangeProfileInfoView(APIView):
    permission_classes = (IsAuthenticatedAndNormalUser,)

    def patch(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed('not authenticated')
        user = request.user
        if user.is_staff:
            response = {'message': "staff users do not have a profile"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        try:
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            phone_number = request.data['phone_number']
            avatar = request.data['avatar']
        except Exception as e:
            response = {'message': f'field error {str(e)}'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(parent_base_user=user)
        if not first_name == '':
            profile.first_name = first_name
        if not last_name == '':
            profile.last_name = last_name
        phone_number_pattern = re.compile(r'^(09)\d{9}$')
        if not phone_number == '':
            if phone_number_pattern.match(phone_number):
                profile.phone_number = phone_number
            else:
                response = {'message': "invalid phone number"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        profile.avatar = avatar
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
