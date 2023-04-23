from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import *


class AddUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = BaseUser
        fields = ('email', 'password')

    def validate(self, attrs):
        validate_password(attrs.get('password'))
        return attrs

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**self.validated_data)
        Profile.objects.create(parent_base_user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(method_name='get_user_type')

    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'is_active', 'date_joined', 'modified_at', 'type')

    def get_user_type(self, base_user):
        if base_user.is_superuser:
            return 'superuser'
        elif base_user.is_staff:
            return 'admin'
        else:
            return 'user'
