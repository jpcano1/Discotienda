""" Album Rating serializer """

# Django Rest Framework
from rest_framework import serializers

# Models
from disco.models import AlbumRating

""" Album rating model serializer """
class AlbumRatingModelSerializer(serializers.ModelSerializer):

    """ Meta Class """
    class Meta:
        model = AlbumRating
        fields = (
            'rating_user',
            'rating',
            'comments'
        )
        # read_only_fields = '__all__'