from django.urls import path, include
from .api import LoanAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('loans', LoanAPI, basename='loans')

urlpatterns = [
    path('', include(router.urls))
]