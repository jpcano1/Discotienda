""" Albums urls """

# Django
from django.urls import path, include

# Views
from .views import albums as album_views

# Django rest framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'albums', album_views.AlbumViewSet, basename='album')

urlpatterns = [
    path('', include(router.urls))
]