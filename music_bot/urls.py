from django.urls import path, include
from rest_framework import routers

from music_bot.views import *

router = routers.DefaultRouter()
router.register('artists', ArtistViewSet)
router.register('albums', AlbumViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
