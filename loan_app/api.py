from rest_framework import viewsets
from .serializers import LoanSerializer
from .models import Loan

class LoanAPI(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer