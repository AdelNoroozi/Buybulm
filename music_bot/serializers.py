from rest_framework import serializers

from music_bot.models import *


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'desc', 'get_plays')
        read_only_fields = ('id', 'get_plays')


class ArtistMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'get_plays')
        read_only_fields = ('id', 'name', 'get_plays')


class SongsInAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'cover', 'artists', 'plays')
        read_only_fields = ('id', 'title', 'cover', 'artists', 'plays')


class AlbumSerializer(serializers.ModelSerializer):
    songs = SongsInAlbumSerializer(many=True)

    class Meta:
        model = Album
        fields = (
            'id', 'title', 'desc', 'release_date', 'artists', 'cover', 'min_price', 'is_public', 'get_plays',
            'songs')
        read_only_fields = ('id', 'get_plays', 'songs')


class AlbumMiniSerializer(serializers.ModelSerializer):
    number_of_songs = serializers.SerializerMethodField(method_name='get_number_of_songs')

    class Meta:
        model = Album
        fields = ('id', 'title', 'artists', 'cover', 'is_public', 'get_plays', 'number_of_songs')
        read_only_fields = ('id', 'title', 'artists', 'cover', 'is_public', 'get_plays', 'number_of_songs')

    def get_number_of_songs(self, album):
        return Song.objects.filter(album=album).count()


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'desc', 'cover', 'artists', 'album', 'file', 'release_date', 'lyrics', 'plays')
        read_only_fields = ('id',)


class SongMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'cover', 'artists', 'album', 'plays')
        read_only_fields = ('id', 'title', 'cover', 'artists', 'album', 'plays')
