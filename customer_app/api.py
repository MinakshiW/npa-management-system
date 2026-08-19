from rest_framework import viewsets
from .serializers import CustomerSerializer
from .models import Customer

class CustomerAPI(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    