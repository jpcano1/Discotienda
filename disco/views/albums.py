""" Album views """

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# Models
from disco.models import Album, AlbumRating
from cancion.models import Song

# Serializers
from disco.serializers import AlbumModelSerializer, AlbumRatingModelSerializer
from cancion.serializers import SongModelSerializer

# Permissions
from disco.permissions import IsCreatorPermission
from rest_framework.permissions import AllowAny, IsAuthenticated

""" Circle View set"""
class AlbumViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin
                   ):

    queryset = Album.objects.all()
    serializer_class = AlbumModelSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            permissions = [IsCreatorPermission]
        elif self.action in ['list', 'retrieve']:
            permissions = [AllowAny]
        elif self.action in ['create']:
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [p() for p in permissions]

    """ Album Detail"""
    def retrieve(self, request, *args, **kwargs):
        response = super(AlbumViewSet, self).retrieve(request, *args, **kwargs)
        ratings = AlbumRating.objects.filter(rated_album=response.data['id'])
        songs = Song.objects.filter(album=response.data['id'])
        data = {
            'album': response.data,
            'ratings': AlbumRatingModelSerializer(ratings, many=True).data,
            'songs': SongModelSerializer(songs, many=True).data
        }
        response.data = data
        return response

    """ Allows to delete the detail of the album """
    def destroy(self, request, *args, **kwargs):
        response = super(AlbumViewSet, self).destroy(request, *args, *kwargs)
        return response
