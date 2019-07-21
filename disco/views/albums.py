""" Album views """

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response

# Models
from disco.models import Album, AlbumRating

# Serializers
from disco.serializers import AlbumModelSerializer, AlbumRatingModelSerializer

""" Circle View set"""
class AlbumViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):

    queryset = Album.objects.all()
    serializer_class = AlbumModelSerializer
    lookup_field = 'pk'

    """ The method that performs the save-object-method """
    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        response = super(AlbumViewSet, self).retrieve(request, *args, **kwargs)
        album = Album.objects.get(title=response.data['title'])
        ratings = AlbumRating.objects.filter(rated_album=album)
        data = {
            'album': response.data,
            'ratings': AlbumRatingModelSerializer(ratings, many=True).data
        }
        response.data = data
        return response
