""" User permissions """

# Django Rest Framework
from rest_framework import permissions

""" Allows acces only to the owner of the account """
class IsAccountOwner(permissions.BasePermission):

    """ Check obj and the user are the same """
    def has_object_permission(self, request, view, obj):
        print("Hola")
        return request.user == obj

class IsAlbumAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj, **kwargs):
        # print(kwargs['sold_by'], request.user)
        return False