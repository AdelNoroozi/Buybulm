from django_filters import FilterSet

from store.models import Payment


class PaymentFilter(FilterSet):
    class Meta:
        model = Payment
        fields = {
            'user': ['exact'],
            'album': ['exact'],
            'payment_time': ['gt', 'lt'],
            'price': ['gt', 'lt'],
            'status': ['exact']
        }
