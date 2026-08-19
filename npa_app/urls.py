from django.urls import path, include
from .api import NPAAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('npa', NPAAPI, basename='npa')

urlpatterns = [
    path('', include(router.urls)),
]