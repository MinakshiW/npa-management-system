from django.urls import path, include
from .api import RecoveryAssignmentAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recovery_assignment', RecoveryAssignmentAPI, basename='recovery_assignment')

urlpatterns = [
    path('', include(router.urls))
]