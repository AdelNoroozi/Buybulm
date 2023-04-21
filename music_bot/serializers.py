from rest_framework import serializers

from music_bot.models import *


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'desc')
        read_only_fields = ('id',)


class ArtistMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'desc', 'release_date', 'artists', 'cover', 'min_price')
        read_only_fields = ('id',)


class AlbumMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'artists', 'cover')
        read_only_fields = ('id', 'title', 'artists', 'cover')


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'desc', 'cover', 'artists', 'album', 'release_date', 'lyrics', 'plays')
        read_only_fields = ('id',)


class SongMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'cover', 'artists', 'album', 'plays')
        read_only_fields = ('id', 'title', 'cover', 'artists', 'album', 'plays')
