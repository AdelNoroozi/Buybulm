from django.urls import path, include
from rest_framework import routers

from music_bot.views import *

router = routers.DefaultRouter()
router.register('artists', ArtistViewSet, basename='Artist')
router.register('albums', AlbumViewSet, basename='Album')
router.register('songs', SongViewSet, basename='Song')

urlpatterns = [
    path('', include(router.urls)),
]
