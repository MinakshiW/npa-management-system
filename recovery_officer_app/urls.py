from django.urls import path, include
from .api import RecoveryOfficerAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recovery_officer', RecoveryOfficerAPI, basename='recovery_officer')

urlpatterns = [
    path('', include(router.urls))
]