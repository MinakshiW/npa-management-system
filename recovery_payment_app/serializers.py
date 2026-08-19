from rest_framework import serializers 
from .models import RecoverPayment
from django.db import transaction
from django.core.cache import cache
from .tasks import send_payment_notification

class RecoverPaymentSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        read_only = True,
        format = "%d/%m/%Y %H:%M:%S"
    )

    updated_at = serializers.DateTimeField(
            read_only = True,
            format = "%d/%m/%Y %H:%M:%S"
        )

    class Meta:

        model = RecoverPayment

        fields = '__all__'

        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]

    @transaction.atomic
    def create(self, validated_data):

        npa = validated_data['npa']
        loan = npa.loan
        payment_amount = validated_data['payment_amount']

        if payment_amount > loan.outstanding_amount:
            raise serializers.ValidationError(
                'Payment cannot exceed outstanding amount.....'
            )

        loan.outstanding_amount -= payment_amount

        if loan.outstanding_amount == 0:
            loan.loan_status = 'closed'
            npa.recovery_status = 'recovered'
        else:
            npa.recovery_status = 'in_progress'

        loan.save()
        npa.save()

        transaction.on_commit(
            lambda : cache.delete_pattern(f"npa_detail_{npa.id}")
        )

        payment = RecoverPayment.objects.create(**validated_data)

        print("PAYMENT CREATED:", payment.id)

        transaction.on_commit(
            lambda: send_payment_notification.delay(payment.id)
        )

        print("CELERY TASK SENT:", payment.id)

        return payment

    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            'Recovery payments cannot be modified once created....'
        )