""" User Rating model """

# Django
from django.db import models

# Utilities
from utils.models import RatingModel

class UserRating(RatingModel):
    """ User Rating model """

    rated_user = models.ForeignKey('users.User',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   related_name="rated_user")

    rating_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name="rating_user"
    )

    def __str__(self):
        """ Returns the rated user """
        return "{user} rated with: {rate}".format(user=str(self.rated_user), rate=self.rating)