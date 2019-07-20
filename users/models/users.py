""" User model, here we're gonna manage new properties for
the attributes of the new user with Abstract Base User Instead """

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from utils.models import DiscotiendaModel, RatingModel

class User(DiscotiendaModel, AbstractUser):
    """ User model based on abstract user,
        This validates an email regex and also validates
        the default username is the email field.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages=
        {
            'unique': 'A user with that email already exists',
        }
    )

    phone_regex = RegexValidator(
        regex=r'^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$',
        message='Invalid phone number format'
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        unique=True,
        max_length=17,
        default=None
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    is_verified = models.BooleanField(
        'Verified',
        default=False,
        help_text='Set to true when the user is verified'
    )

    def __str__(self):
        """ Returns username """
        return self.username

    def get_short_name(self):
        """ Returns short name """
        return "{first_name} - {username}".format(first_name=self.first_name, username=self.username)