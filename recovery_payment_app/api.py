from rest_framework import viewsets
from .models import RecoverPayment
from .serializers import RecoverPaymentSerializer

class RecoveryPaymentAPI(viewsets.ModelViewSet):

    queryset = RecoverPayment.objects.all()
    serializer_class = RecoverPaymentSerializer

    