""" User permissions """

# Django Rest Framework
from rest_framework import permissions

# Models
from disco.models import Album
from cancion.models import Song

""" Allows acces only to the owner of the account """
class IsAccountOwner(permissions.BasePermission):

    """ Check obj and the user are the same """
    def has_object_permission(self, request, view, obj):
        return request.user == obj and request.user.is_verified

    def has_permission(self, request, view):
        if request.user.id == int(view.kwargs['id']):
            return True
        else:
            return False

""" This permission class is defined to allow users to access their albums
if they are the owners 
"""
class IsRequestAccountOwner(permissions.BasePermission):

    """ Allows permission only to the user accesing his own album
    """
    def has_permission(self, request, view, **kwargs):
        if (int(view.kwargs['user']) == request.user.id) and request.user.is_verified:
            return True
        return False

""" Permissions that allows the album creator access the detail with de respective kwarg """
class IsAlbumOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            Album.objects.get(sold_by=view.kwargs['user'], id=view.kwargs['pk'])
            return True
        except Album.DoesNotExist:
            return False

class IsAlbumSong(permissions.BasePermission):

    def has_permission(self, request, view):
        album = view.kwargs['album']
        song = view.kwargs['pk']
        try:
            Song.objects.get(album=album, id=song)
            return True
        except Song.DoesNotExist:
            return False