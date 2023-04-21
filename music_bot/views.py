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
