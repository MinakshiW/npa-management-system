from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        format= '%d/%m/%Y %H-%M-%S', 
        read_only= True
    )

    updated_at = serializers.DateTimeField(
        format= '%d/%m/%Y %H-%M-%S', 
        read_only= True
    )

    class Meta:
        model = Customer
        fields = [
            'id',
            'customer_code',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'date_of_birth',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]
