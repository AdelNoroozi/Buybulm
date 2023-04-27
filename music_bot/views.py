from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from accounts.permissions import BotPermission
from music_bot.models import *
from music_bot.serializers import *


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    permission_classes = (BotPermission,)
    filter_backends = [SearchFilter, ]
    search_fields = ['name', 'desc']
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ArtistMiniSerializer
        else:
            return ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = (BotPermission,)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'desc', 'artists__name']
    ordering_fields = ['release_date', 'min_price']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        albums = Album.objects.all()
        sorted_results = sorted(albums, key=lambda a: a.get_plays())
        return sorted_results

    def get_serializer_class(self):
        if self.action == 'list':
            return AlbumMiniSerializer
        else:
            return AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    permission_classes = (BotPermission,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'desc', 'artists__name', 'album__title', 'lyrics']
    ordering_fields = ['release_date', 'plays']

    def get_serializer_class(self):
        if self.action == 'list':
            return SongMiniSerializer
        else:
            return SongSerializer
