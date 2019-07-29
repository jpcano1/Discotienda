""" User serializer """

# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Django Rest framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Serializers
from users.serializers.profiles import ProfileModelSerializer
from disco.serializers import AlbumModelSerializer

# Models
from users.models import User, Profile

# Utilities
from jose import jwt
from jose.jwt import *
from django.utils import timezone

""" Account verification Serializer that allows to know which user has a 
verificated account and which doesn't
"""
class AccountVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    """ Validate method for the token """
    def validate(self, data):
        try:
            payload = jwt.decode(data['token'], settings.SECRET_KEY, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise serializers.ValidationError("The token has expired.")
        except JWTError:
            raise serializers.ValidationError("Error validating token. Ensure is the right token.")

        self.context['payload'] = payload
        return data

    """ Update the user's verification status """
    def save(self, **kwargs):
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()

""" Login serializer to make a login to a User """
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=64)

    """ Function that makes the validation email-password """
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("The credentials provided are incorrect")
        if not user.is_verified:
            raise serializers.ValidationError("The user is not verified, please check your email")

        self.context['user'] = user
        return data

    """ Get or create token """
    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        # token = self.gen_token_auth(self.context['user'])
        return self.context['user'], token.key

    """ Generates a token each time the user acces its account """
    def gen_token_auth(self, user):
        payload = {
            'user': user.username,
            'type': 'login_token'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

""" Class that allows us to create users and to send 
verification token to the user through the email. 
"""
class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$',
        message='Invalid phone number format'
    )
    phone_number = serializers.CharField(validators=[phone_regex], required=True)

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # Image
    picture = serializers.ImageField(required=False, default=None)

    def validate(self, data):
        passwd = data['password']
        passwd_confirmation = data['password_confirmation']

        if passwd_confirmation != passwd:
            raise serializers.ValidationError("Passwords don't match")

        password_validation.validate_password(passwd)

        return data

    def create(self, data):
        data.pop('password_confirmation')
        imagen = None
        if data['picture']:
            imagen = data['picture']
        data.pop('picture')
        user = User.objects.create_user(**data)
        Profile.objects.create(user=user, picture=imagen)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """ Send account verification link to given user """
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {
                'token': verification_token,
                'user': user
            }
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach(content, 'text/html')
        msg.send()
        print("Sending email")
        # print(verification_token)

    def gen_verification_token(self, user):
        """ create JWT token that the user can use to verify its account. """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

""" User model serializer will allow me to choose what
fields i'd like to show to the user """
class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)

    """ Meta class """
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'profile',
                  )