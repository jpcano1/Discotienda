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
            'sold_by',
            'quantities',
        )

    """ Validate the user doesn't have repeated albums 
    and cover exists. """
    def validate(self, data):
        # print("Este es el title:", data['title'])
        # print("Este es el vendedor:", data['sold_by'])
        users = data['sold_by']
        for user in users:
            album = Album.objects.filter(title=data['title'], artist=data['artist'],sold_by=user)
            if album:
                raise serializers.ValidationError("Este album ya te pertenece")
        if not data.get('cover'):
            raise serializers.ValidationError("Cover required for confidence to the clients")
        album = Album.objects.filter(title=data['title'], artist=data['artist'])
        if album:
            album.quantities += 1
            album.sold_by.append(data['sold_by'][0])
            album.save()
        return data