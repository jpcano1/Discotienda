""" Album permissions """

# Django REST framework
from rest_framework.permissions import BasePermission

""" Verifies if request user is Creator user """
class IsCreatorPermission(BasePermission):

    """ Gives Permission to the creator of the album """
    def has_object_permission(self, request, view, obj):
        if request.user == obj.sold_by:
            return True
        return False