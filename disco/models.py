""" Album model """

# Django
from django.db import models

# Utilities
from utils.models import DiscotiendaModel, RatingModel

# Create your models here.
class Album(DiscotiendaModel):
    """ Album model that uses attibutes and relations to the user
     and to the songs in it
     """

    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=20)
    cover = models.ImageField(upload_to='album/covers/', null=True, blank=True)

    price = models.FloatField()
    sold_by = models.ManyToManyField('users.User', related_name='album_sold_by')

    quantities = models.IntegerField(default=1)
    sold_unities = models.IntegerField(default=0)

    digital = models.BooleanField(default=False)

    def __str__(self):
        """ returns title and artist """
        return "{title} - written by: {artist}".format(title=self.title, artist=self.artist)

class AlbumRating(RatingModel):
    """ The model to rate an specific album """

    rated_song = models.ForeignKey('Album',
                                   on_delete=models.CASCADE,
                                   related_name="rated_song")

    rating_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name="album_rating_user"
    )

    def __str__(self):
        """ Returns the rate and the album rated """
        return "{album} rated with: {rate}".format(album=str(self.rated_song), rate=self.rating)
