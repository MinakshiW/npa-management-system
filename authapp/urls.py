from django.urls import path
from .api import LogoutAPI

urlpatterns = [
    path('logout', LogoutAPI.as_view, name='logout')
]