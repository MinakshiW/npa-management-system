from rest_framework import serializers
from .models import RecoveryOfficer

class RecoveryOfficerSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        read_only = True,
        format='%d/%m/%Y %H:%M:%S'
    )

    updated_at = serializers.DateTimeField(
        read_only = True,
        format='%d/%m/%Y %H:%M:%S'
    )

    class Meta:

        model = RecoveryOfficer
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]

    def validate_phone(self, value):
        if len(value) !=10 or not value.isdigit():
            raise serializers.ValidationError(
                'Phone number must be exactly 10 digits....'
            )
        return value

    def validate_employee_id(self, value):
        if not value.startswith('EMP'):
            raise serializers.ValidationError(
                'Employee ID must start with EMP....'
            )
        return value

    def validate_email(self, value):
        if not value.endswith('@bank.com'):
            raise serializers.ValidationError(
                'Please use an official bank email address....'
            )
        return value