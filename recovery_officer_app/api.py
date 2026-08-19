from rest_framework import viewsets
from .models import RecoveryOfficer
from .serializers import RecoveryOfficerSerializer
from .permission import IsRecoveryOfficer

class RecoveryOfficerAPI(viewsets.ReadOnlyModelViewSet):

    serializer_class = RecoveryOfficerSerializer
    permission_classes = [IsRecoveryOfficer]

    def get_queryset(self):

        user = self.request.user

        if not user.is_authenticated:
            return RecoveryOfficer.objects.none()

        if not hasattr(user, 'recovery_officer'):
            return RecoveryOfficer.objects.none()
        
        return RecoveryOfficer.objects.filter(user=user)
    