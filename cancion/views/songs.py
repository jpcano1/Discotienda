""" Song's views """

# Django rest framework
from rest_framework import viewsets, mixins

# Models
from cancion.models import Song, SongRating

# Serializer
from cancion.serializers import SongModelSerializer

""" Song view set that allows me create a song, that's the only thing needed """
class SongViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """"""

    queryset = Song.objects.all()
    serializer_class = SongModelSerializer

    def perform_create(self, serializer):
        serializer.save()