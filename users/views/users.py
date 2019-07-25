""" Users views """

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Models
from users.models import User, Profile
from disco.models import Album
from cancion.models import Song

# Serializer
from users.serializers import (UserModelSerializer,
                               LoginSerializer,
                               AccountVerificationSerializer,
                               UserSignUpSerializer)
from users.serializers.profiles import ProfileModelSerializer
from disco.serializers import AlbumModelSerializer, CreateAlbumSerializer
from cancion.serializers import SongModelSerializer, SongCreationSerializer


# Permissions
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)
from users.permissions import IsAccountOwner, IsRequestAccountOwner, IsAlbumOwner, IsAlbumSong

""" User viewset in which I'm going to make the views for a
CRUD system for users based on permissions, handles signup,
login, verify account etc...
"""
class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'id'

    """ Method that defines permission for each action """
    def get_permissions(self):
        if self.action in ['signup', 'login', 'verify', 'list', 'retrieve']:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    """ The retrieve mixin view, allows to see the user detail """
    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        albums = Album.objects.filter(
            sold_by=response.data['id']
        )
        data = {
            'user': response.data,
            'albums': AlbumModelSerializer(albums, many=True).data
        }
        response.data = data
        return response

    """ The list mixin view """
    def list(self, request, *args, **kwargs):
        response = super(UserViewSet, self).list(request, *args, **kwargs)
        return response

    """ User's login view """
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    """ Verifies an profile through token validation """
    @action(detail=False, methods=['post'])
    def verify(self, request):
        """  """
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"Message": "Congratulations, now go check some new albums!!!"}
        return Response(data, status=status.HTTP_200_OK)

    """ Creates an user in the database with is_verified value = False """
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    """ Method that allow to profile-owner to update its information """
    # def update(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     profile = user.profile
    #     partial = request.method == 'PATCH'
    #     serializer = ProfileModelSerializer(
    #         profile,
    #         data=request.data,
    #         partial=partial
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     data = UserModelSerializer(user).data
    #     return Response(data)

    # @action(detail=True, methods=['get'])
    # def profile(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     albums = Album.objects.filter(sold_by=user)
    #     data = {
    #         'user': UserModelSerializer(user).data,
    #         'albums': AlbumModelSerializer(albums, many=True).data
    #     }
    #     return Response(data)

class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin):

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'retrieve']:
            permissions = [IsAccountOwner, IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        albums = Album.objects.filter(sold_by=user)
        data = {
            'user': UserModelSerializer(user).data,
            'albums': AlbumModelSerializer(albums, many=True).data
        }
        return Response(data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

""" Thi view set is defined to allow users to create, read, update and destroy his albums """
class UserAlbumViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin):

    serializer_class = AlbumModelSerializer
    queryset = Album.objects.all()

    """ Class that sets permissions based on the actions """
    def get_permissions(self):
        if self.action in ['create', 'list', 'destroy']:
            permissions = [IsRequestAccountOwner]
        elif self.action in ['retrieve']:
            permissions = [IsAlbumOwner, IsRequestAccountOwner]
        elif self.action in ['update', 'partial_update']:
            permissions = [IsAlbumOwner, IsRequestAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        id = kwargs['user']
        self.user = get_object_or_404(
            User,
            id=id
        )
        return super(UserAlbumViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = self.user
        albums = Album.objects.filter(sold_by=user)
        data = {
            'albums': AlbumModelSerializer(albums, many=True).data
        }
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        user = self.user
        albums = Album.objects.filter(sold_by=user)
        albums.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        user = self.user
        request.data['sold_by'] = user.id
        serializer = CreateAlbumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = serializer.save()
        data = AlbumModelSerializer(album).data
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        album = self.get_object()
        request.data['sold_by'] = self.user.id
        partial = request.method == 'PATCH'
        serializer = AlbumModelSerializer(
            album,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = AlbumModelSerializer(album).data
        return Response(data, status=status.HTTP_200_OK)

""" Class that allows me to manage song's CRUD """
class UserAlbumSongViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin):
    """"""
    serializer_class = SongModelSerializer
    queryset = Song.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permissions = [IsRequestAccountOwner, IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permissions = [IsAlbumSong, IsRequestAccountOwner]
        else:
            permissions = []
        return [p() for p in permissions]

    def update(self, request, *args, **kwargs):
        song = self.get_object()
        request.data['album'] = self.album.id
        partial = request.method == 'PATCH'
        serializer = SongModelSerializer(
            song,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = SongModelSerializer(song).data
        return Response(data)

    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs['user']
        album_id = kwargs['album']
        self.user = get_object_or_404(User, id=user_id)
        self.album = get_object_or_404(Album, id=album_id, sold_by=self.user)
        return super(UserAlbumSongViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        album = self.album
        request.data['album'] = album.id
        serializer = SongCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        song = serializer.save()
        data = SongModelSerializer(song).data
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        album = self.album
        songs = Song.objects.filter(album=album.id)
        data = {
            'songs': SongModelSerializer(songs, many=True).data
        }
        return Response(data)