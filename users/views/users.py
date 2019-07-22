""" Users views """

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Models
from users.models import User
from disco.models import Album

# Serializer
from users.serializers import (UserModelSerializer,
                               LoginSerializer,
                               AccountVerificationSerializer,
                               UserSignUpSerializer)
from users.serializers.profiles import ProfileModelSerializer
from disco.serializers import AlbumModelSerializer


# Permissions
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)
from users.permissions import IsAccountOwner, IsAlbumAccountOwner

""" User viewset in which I'm going to make the views for a
CRUD system for users based on permissions, handles signup,
login, verify account etc...
"""
class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['update', 'partial_update']:
            permissions = [IsAccountOwner, IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    """ The retrieve mixin view, allows to see the user detail """
    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        albums = Album.objects.filter(
            sold_by=request.user
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

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """  """
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"Message": "Congratulations, now go check some new albums!!!"}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
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

class UserAlbumViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.CreateModelMixin):

    serializer_class = UserModelSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permissions = [IsAlbumAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        id = kwargs['id']
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
        request.data['sold_by'] = self.user
        return Response({'hola': 'hola'})