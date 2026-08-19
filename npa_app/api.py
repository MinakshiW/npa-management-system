from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.cache import cache

from .serializers import NPASerializer
from .models import NPA
from recovery_officer_app.permission import IsRecoveryOfficer

import logging

logger = logging.getLogger(__name__)
 
class NPAAPI(viewsets.ReadOnlyModelViewSet):
    
    serializer_class = NPASerializer

    permission_classes = [IsAuthenticated, IsRecoveryOfficer]

    #to get version
    def list(self, request, *args, **kwargs):

        print("API VERSION:", request.version)

        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        

        user = self.request.user

        logger.info(
            'NPA requested by user = %s', 
            self.request.user.id
        )

        return NPA.objects.filter(
            assignments__recovery_officer__user=user,
            assignments__assignment_status="active"

        ).distinct()

    def retrieve(self, request, *args, **kwargs):

        npa_id = kwargs.get("pk")

        cache_key = f"npa_detail_{npa_id}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:

            print("CACHE HIT")

            return Response(cached_data)

        print("CACHE MISS")

        response = super().retrieve(request, *args, **kwargs)

        cache.set(
            cache_key,
            response.data,
            timeout=300
        )

        return response