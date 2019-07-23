""" Song's urls """

# Django Rest Framerwork
from rest_framework.routers import DefaultRouter

# Django
from django.urls import path, include

# Views
from .views import songs as songs_views

router = DefaultRouter()
router.register(r'albums/(?P<album>[0-9]+)/songs', songs_views.SongViewSet, basename='songs')

urlpatterns = [
    path('', include(router.urls))
]