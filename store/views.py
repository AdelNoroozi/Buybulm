from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.models import Profile
from music_bot.models import Album
from store.filters import PaymentFilter
from store.models import Payment
from store.serializers import PaymentSerializer, PaymentMiniSerializer


class CreatePaymentView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            response = {'message': 'user is not authenticated'}
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        if user.is_staff:
            response = {'message': 'staff users can not buy albums'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if not Profile.objects.filter(parent_base_user=user).exists():
            # if everything goes right, this condition won't occur at all.
            # this if statement just makes sure that nothing unexpected has happened.
            response = {'message': 'profile does not exist for this user'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(parent_base_user=user)
        try:
            album_id = request.data['album_id']
            suggesting_price = request.data['suggesting_price']
            user_preview_name = request.data['user_preview_name']
            message = request.data['message']
        except Exception as e:
            response = {'message': f'field error: {str(e)}'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        try:
            int(album_id)
        except:
            response = {'message': 'invalid album id'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if not Album.objects.filter(id=album_id).exists():
            response = {'message': 'album not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        album = Album.objects.get(id=album_id)
        if Payment.objects.filter(user=profile, album=album).exists():
            response = {'message': 'you have already bought this album'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        try:
            suggesting_price_float = float(suggesting_price)
        except:
            response = {'message': 'invalid suggesting price'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if suggesting_price_float < album.min_price:
            response = {'message': 'your suggesting price is less than albums minimum price'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if user_preview_name == '':
            response = {'message': 'user preview name can not be empty'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.create(user=profile, album=album, price=suggesting_price, message=message,
                                         user_preview_name=user_preview_name, status='RTP')
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_time', 'price']

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentMiniSerializer
        else:
            return PaymentSerializer

    @action(detail=True, methods=['PATCH', ])
    def change_payment_status(self, request, pk=None):
        if not Payment.objects.filter(id=pk).exists():
            response = {'message': 'payment not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        try:
            payment_status = request.data['status']
        except Exception as e:
            response = {'message': f'field error: {str(e)}'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.get(id=pk)
        if payment_status == payment.status:
            response = {'message': f'this payment is already in {payment_status} status'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if (payment_status != 'P') and (payment_status != 'FC') and (payment_status != 'RTP') and (
                payment_status != 'R'):
            response = {'message': 'invalid status'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if payment_status == 'P':
            try:
                receipt = request.data['receipt']
            except Exception as e:
                response = {'message': f'field error: {str(e)}'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            payment.receipt = receipt
        elif payment_status == 'FC':
            # send files
            pass
        payment.status = payment_status
        payment.save()
        response = {'message': 'status changed successfully'}
        return Response(response, status=status.HTTP_200_OK)
