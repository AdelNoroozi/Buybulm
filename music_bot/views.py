from django.db.models import Sum
from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from accounts.models import Profile
from accounts.permissions import BotPermission, IsAuthenticated, PlaySongPermission
from music_bot.filters import AlbumFilter, SongFilter
from music_bot.models import *
from music_bot.serializers import *
from store.models import Payment


class ArtistViewSet(viewsets.ModelViewSet):
    permission_classes = (BotPermission,)
    filter_backends = [SearchFilter, ]
    search_fields = ['name', 'desc']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Artist.objects.annotate(total_play=Sum('songs__plays')).order_by('-total_play')

    def get_serializer_class(self):
        if self.action == 'list':
            return ArtistMiniSerializer
        else:
            return ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = (BotPermission,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AlbumFilter
    search_fields = ['title', 'desc', 'artists__name']
    ordering_fields = ['release_date']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Album.objects.annotate(total_play=Sum('songs__plays')).order_by('-total_play')

    def get_serializer_class(self):
        if self.action == 'list':
            return AlbumMiniSerializer
        else:
            return AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    permission_classes = (BotPermission,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SongFilter
    search_fields = ['title', 'desc', 'artists__name', 'album__title', 'lyrics']
    ordering_fields = ['release_date', 'plays']

    def get_serializer_class(self):
        if self.action == 'list':
            return SongMiniSerializer
        else:
            return SongSerializer

    @action(detail=True, methods=['PATCH', ], permission_classes=[BotPermission])
    def add_play(self, request, pk=None):
        if not Song.objects.filter(id=pk).exists():
            response = {'message': 'song not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        song = Song.objects.get(id=pk)
        if not song.album.is_public:
            try:
                profile = Profile.objects.get(parent_base_user=request.user)
            except:
                response = {'message': 'no profile found for this user'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            if not Payment.objects.filter(user=profile, album=song.album).exists():
                response = {'message': 'you do not have access to this album'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
        song.plays += 1
        song.save()
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)
