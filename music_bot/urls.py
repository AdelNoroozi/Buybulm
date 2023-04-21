from django.urls import path, include
from rest_framework import routers

from music_bot.views import ArtistViewSet

router = routers.DefaultRouter()
router.register('artists', ArtistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
