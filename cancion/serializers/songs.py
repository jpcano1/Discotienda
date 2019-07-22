""" Song's Serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from cancion.models import Song

""" Song model serializer """
class SongModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('title',
                  'minutes',
                  'seconds',
                  'album',
                  'price')

    """ Validate all data before creation """
    def validate(self, data):
        album = data['album']
        title = data['title']
        song = Song.objects.filter(album=album, title=title)

        if song:
            raise serializers.ValidationError("This song is already in the album")

        return data
