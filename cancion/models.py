""" Song's models"""

# Django
from django.db import models

# Utilities
from utils.models import DiscotiendaModel, RatingModel

class Song(DiscotiendaModel):
    """ Song model that stores information about a song that's going to be sold in the
        platform
    """

    title = models.CharField(max_length=255)
    minutes = models.IntegerField(default=1)
    seconds = models.FloatField(default=1)
    album = models.ForeignKey('disco.Album',
                              on_delete=models.CASCADE,
                              related_name="album")

    sold_unities = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)

    def __str__(self):
        """ Returns the title and the album """
        return "{title} in album: {album}".format(title=self.title, album=str(self.album))

class SongRating(RatingModel):
    """ Model that defines the ratings to songs """

    rated_song = models.ForeignKey('Song',
                                   on_delete=models.CASCADE,
                                   related_name="rated_song")

    rating_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name="song_rating_user"
    )
    def __str__(self):
        """ Returns the song and the rating """
        return "{song} rated with: {rate}".format(song=str(self.rated_song), rate=self.rating)


