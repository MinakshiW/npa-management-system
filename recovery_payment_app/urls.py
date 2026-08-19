from django.urls import path, include
from .api import RecoveryPaymentAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recovery_payment', RecoveryPaymentAPI, basename='recovery_payment')

urlpatterns = [
    path('', include(router.urls))
]