""" Profile Models """

# Django
from django.db import models

# Utilities
from utils.models import DiscotiendaModel

class Profile(DiscotiendaModel):
    """ Profile model that makes explicit the model of one's user """
    user = models.OneToOneField('User', on_delete=models.CASCADE)

    picture = models.ImageField(
        'Profile image',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )

    biography = models.CharField(max_length=500, blank=True)

    adquired_albums = models.PositiveIntegerField(default=0)
    sold_albums = models.PositiveIntegerField(default=0)

    reputation = models.FloatField(default=5.0)

    def __str__(self):
        """ Returns usename """
        return str(self.user)
