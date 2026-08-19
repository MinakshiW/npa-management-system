from rest_framework import serializers
from .models import NPA
from django.db import transaction

class NPASerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        read_only = True,
        format = '%d/%m/%Y %H-%M-%S'
    )

    updated_at = serializers.DateTimeField(
        read_only = True,
        format = '%d/%m/%Y %H-%M-%S'
    )

    class Meta:

        model = NPA
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]

    def validate_days_past_due(self, value):

        if value < 90:
            raise serializers.ValidationError(
                "Loan cannot be marked as NPA before 90 days past due.."
            )
        
        return value


    @transaction.atomic   #ensures that all database operations inside the function are treated as a single transaction.
    def create(self, validated_data):

        loan =  validated_data['loan']
        dpd = validated_data['days_past_due']

        #change npa_category as per business rule
        if dpd <= 365:
            validated_data['npa_category'] = 'substandard'
        elif dpd <= 730:
            validated_data['npa_category'] = 'doubtful'
        else:
            validated_data['npa_category'] = 'loss'

        #change loan status if npa is being create
        if loan.loan_status == 'npa':
            raise serializers.ValidationError(
                "This loan is already marked as npa..."
            )
        elif loan.loan_status == 'closed':
            raise serializers.ValidationError(
                'Cannot create NPA for closed loan..'
            )
        else:
            loan.loan_status = 'npa'   

        loan.save()

        return NPA.objects.create(**validated_data)