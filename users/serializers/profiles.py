""" Profile model serializer.
    will allow me to decide the fields
    I want to show
"""

# Django Rest Framework
from rest_framework import serializers

# Models
from users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """ Profile Model serializer """
    class Meta:
        """ Class Meta """
        model = Profile
        fields = ('picture',
                  'biography',
                  'adquired_albums',
                  'sold_albums',
                  'reputation')
        read_only_fields = ('adquired_albums',
                            'sold_albums',
                            'adquired_albums')