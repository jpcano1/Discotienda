""" Abstract model that stores the creation and modification date """

# Django
from django.db import models

class DiscotiendaModel(models.Model):
    """ Discotienda model """

    created_at = models.DateTimeField(
        'Created at field',
        auto_now_add=True,
        help_text="Date time in which the object was created"
    )

    modified_at = models.DateTimeField(
        'Modified at field',
        auto_now=True,
        help_text='Date time in which the object was modified'
    )

    class Meta:
        """ class meta """

        abstract = True
        ordering = ['-created_at', '-modified_at']

        get_latest_by = 'created_at'

class RatingModel(DiscotiendaModel):
    """ Ratings model """

    rating = models.FloatField(default=1.0)
    comments = models.TextField(blank=True)

    class Meta:
        """ Class Name """
        abstract = True

        get_latest_by = 'created_at'
        ordering = ['-created_at', '-modified_at', '-rating']