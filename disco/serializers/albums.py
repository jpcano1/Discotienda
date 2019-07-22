""" Album serializer """

# Django Rest Framework
from rest_framework import serializers

# Models
from disco.models import Album

# Serializers
from .ratings import AlbumRatingModelSerializer

""" Album model serializer """
class AlbumModelSerializer(serializers.ModelSerializer):

    ratings = AlbumRatingModelSerializer(read_only=True, many=True)
    """ Meta Class """
    class Meta:
        model = Album
        fields = (
            'id',
            'title',
            'artist',
            'genre',
            'cover',
            'price',
            'sold_by',
            'ratings'
        )

    def validate_title(self, data):
        album = Album.objects.filter(title=data)
        if album:
            raise serializers.ValidationError("Este album ya existe")
        return data