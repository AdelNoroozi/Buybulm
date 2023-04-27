from django_filters.rest_framework import FilterSet
from .models import Album, Song


class AlbumFilter(FilterSet):
    class Meta:
        model = Album
        fields = {
            'min_price': ['gt', 'lt'],
            'artists': ['exact'],

        }


class SongFilter(FilterSet):
    class Meta:
        model = Song
        fields = {
            'artists': ['exact'],
            'album': ['exact'],
        }
