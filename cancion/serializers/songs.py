""" Song's Serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from cancion.models import Song
from disco.models import Album

""" Song model serializer """
class SongModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('id',
                  'title',
                  'album',
                  'price',
                  'minutes',
                  'seconds'
                  )

""" Song creation serializer, allows me to create new Songs in a determinated user-album """
class SongCreationSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=255, required=True)
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), required=True)
    price = serializers.FloatField()
    minutes = serializers.IntegerField()
    seconds = serializers.FloatField()

    """ Validate all data before creation """
    def validate(self, data):
        album = data['album']
        title = data['title']
        song = Song.objects.filter(album=album, title=title)

        if song:
            raise serializers.ValidationError("This song is already in the album")
        return data

    def create(self, data):
        song = Song.objects.create(**data)
        return song

