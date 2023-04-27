from rest_framework import serializers

from store.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'album', 'payment_time', 'price', 'receipt', 'message', 'user_preview_name', 'status')
        read_only_fields = ('id', 'user', 'album', 'payment_time', 'price', 'receipt', 'message', 'user_preview_name')


class PaymentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'album', 'payment_time', 'price', 'status')
        read_only_fields = ('id', 'user', 'album', 'payment_time', 'price', 'status')
