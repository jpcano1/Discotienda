""" Album serializer """

# Django Rest Framework
from rest_framework import serializers

# Models
from disco.models import Album

# Serializers
from .ratings import AlbumRatingModelSerializer

""" Album model serializer """
class AlbumModelSerializer(serializers.ModelSerializer):

    """ Meta Class """
    class Meta:
        model = Album
        fields = (
            'title',
            'artist',
            'genre',
            'cover',
            'price',
            'sold_by'
        )

    """ Validate the user doesn't have repeated albums
    and cover exists. """
    def validate_title(self, data):
        album = Album.objects.get(title=data)
        if album:
            raise serializers.ValidationError("Este album ya existe")
        return data