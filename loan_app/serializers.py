from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        read_only = True,
        format = '%d/%m/%Y %H:%M:%S'
    )

    updated_at = serializers.DateTimeField(
        read_only = True,
        format = '%d/%m/%Y %H:%M:%S'
    )

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]