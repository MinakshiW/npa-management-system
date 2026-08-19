from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from recovery_officer_app.models import RecoveryOfficer
from recovery_officer_app.permission import IsRecoveryOfficer

from .models import RecoveryAssignment
from .serializers import RecoveryAssignmentSerializer


class RecoveryAssignmentAPI(viewsets.ModelViewSet):

    serializer_class = RecoveryAssignmentSerializer


    def get_queryset(self):

        user = self.request.user

        return RecoveryAssignment.objects.filter(
            recovery_officer__user = user
        )

    #resassigned to new employee if old one inactive
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def reassign(self, request, pk=None):

        assignment = self.get_object()

        if assignment.assignment_status != "active":
            return Response(
                {"error": "Only active assignments can be reassigned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if assignment.npa.recovery_status == "closed":
            return Response(
                {"error": "Cannot reassign a closed NPA."},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        old_officer  = assignment.recovery_officer
        officer_id = request.data.get("recovery_officer")

        if not officer_id:
            return Response(
                {"error": "recovery_officer is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        new_officer = get_object_or_404(RecoveryOfficer, id = officer_id)

        if new_officer.status != "active":
            return Response(
                {"error": "Officer is inactive."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if assignment.recovery_officer == new_officer:
            return Response(
                {"error": "This officer is already assigned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        assignment.assignment_status = 'reassigned'
        assignment.remarks = (
            assignment.remarks or ""
            ) + f"\nReassigned to {new_officer.employee_id}"
        assignment.save()

        new_assignment = RecoveryAssignment.objects.create(
            npa = assignment.npa,
            recovery_officer = new_officer,
            assigned_date = timezone.now().date(),
            due_date = request.data.get("due_date"),
            assignment_status = "active",
            remarks = request.data.get("remarks", f"Reassigned from {old_officer.employee_id}") 
        )

        serializer = self.get_serializer(new_assignment)

        return Response(
            {
                "message": "Recovery officer reassigned successfully.",
                'old_officer': old_officer.employee_id,
                'new_officer' : new_officer.employee_id,
                'data' : serializer.data
            },        
            status=status.HTTP_201_CREATED
        )
        