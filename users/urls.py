""" Users urls"""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename="users")
# router.register(r'users/(?P<username>[a-zA-Z0-9_-]+)/albums', user_views.UserAlbumViewSet, basename='users_albums')
router.register(r'users/(?P<id>[0-9]+)/albums', user_views.UserAlbumViewSet, basename='users_albums')

urlpatterns = [
    path('', include(router.urls))
]