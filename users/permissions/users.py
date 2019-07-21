""" User permissions """

# Django Rest Framework
from rest_framework import permissions

""" Allows acces only to the owner of the account """
class IsAccountOwner(permissions.BasePermission):

    """ Check obj and the user are the same """
    def has_object_permission(self, request, view, obj):
        return request.user == obj

