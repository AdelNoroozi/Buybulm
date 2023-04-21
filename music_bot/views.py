from django.shortcuts import render
from rest_framework import viewsets

from music_bot.models import *
from music_bot.serializers import *


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ArtistMiniSerializer
        else:
            return ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AlbumMiniSerializer
        else:
            return AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SongMiniSerializer
        else:
            return SongSerializer
