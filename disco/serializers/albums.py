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

""" Serializer that allows me to create an album """
class CreateAlbumSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=255)
    artist = serializers.CharField(max_length=255)

    sold_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    genre = serializers.CharField(max_length=20)
    cover = serializers.ImageField()

    price = serializers.FloatField()

    sold_unities = serializers.IntegerField(default=0)

    def validate_title(self, data):
        album = Album.objects.filter(title=data)
        if album:
            raise serializers.ValidationError("Este album ya existe")
        return data