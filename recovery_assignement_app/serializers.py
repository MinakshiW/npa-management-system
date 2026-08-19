from rest_framework import serializers
from .models import RecoveryAssignment
from django.db import transaction

import logging

logger = logging.getLogger(__name__)

class RecoveryAssignmentSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        read_only = True,
        format = '%d/%m/%Y %H:%M:%S'
    )

    updated_at = serializers.DateTimeField(
            read_only = True,
            format = '%d/%m/%Y %H:%M:%S'
        )

    class Meta:

        model = RecoveryAssignment
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]

    @transaction.atomic
    def create(self, validated_data):

        npa_id = validated_data['npa'].id

        npa = NPA.objects.select_for_update().get(
            id = npa_id
        )

        officer = validated_data['recovery_officer']

        #closed npa cannot be assigned
        if npa.recovery_status == 'closed':
            raise serializers.ValidationError(
                'Cannot Assigned a closed npa....'
            )

        #only active officers can get assigned
        if officer.status != 'active':

            logger.warning(
                'Attemp to assign inactive officer=%s to NPA=%s',
                officer.employee_id,
                npa.id
            )

            raise serializers.ValidationError(
                'Inactive officers cannot get assigned....'
            )

        #one npa only one active assignement    
        assignment_exist = RecoveryAssignment.objects.filter(
            npa = npa,
            assignment_status = 'active',
        ).exists()

        if assignment_exist:
             
            raise serializers.ValidationError(
                "This NPA already has an active Recovery Officer...."
            )   

        return RecoveryAssignment.objects.create(**validated_data)

    