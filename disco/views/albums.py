""" Album views """

# Django REST Framework
from rest_framework import viewsets, mixins

# Models
from disco.models import Album

# Serializers
from disco.serializers import AlbumModelSerializer

""" Circle View set"""
class AlbumViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin):

    queryset = Album.objects.all()
    serializer_class = AlbumModelSerializer
    lookup_field = 'pk'

    """ The method that performs the save-object-method """
    def perform_create(self, serializer):
        serializer.save()
