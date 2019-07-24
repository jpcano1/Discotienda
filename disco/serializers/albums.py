""" Album serializer """

# Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from disco.models import Album
from users.models import User

# Serializers
from .ratings import AlbumRatingModelSerializer

""" Album model serializer """
class AlbumModelSerializer(serializers.ModelSerializer):

    ratings = AlbumRatingModelSerializer(read_only=True, many=True)
    cover = serializers.ImageField(required=False)

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

        read_only_fields = ('ratings',
                            'sold_by')

""" Serializer class that allows me to create an album """
class CreateAlbumSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255,
        validators=[
            UniqueValidator(queryset=Album.objects.all())
        ]
    )
    artist = serializers.CharField(
        max_length=255
    )
    genre = serializers.CharField(
        max_length=255
    )
    cover = serializers.ImageField(required=False)
    price = serializers.FloatField()

    sold_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    ratings = AlbumRatingModelSerializer(read_only=True, many=True)

    def validate(self, data):
        title = data['title']
        album = Album.objects.filter(title=title)
        if album:
            raise serializers.ValidationError("Este album ya existe")
        return data

    def create(self, data):
        album = Album.objects.create(**data)
        return album