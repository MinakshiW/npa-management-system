from django.urls import path, include
from .api import CustomerAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('customer', CustomerAPI, basename='customer')

urlpatterns = [
    path("", include(router.urls))   
]