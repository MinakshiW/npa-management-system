from django.db import models
from npa_app.models import NPA
from recovery_officer_app.models import RecoveryOfficer

class RecoveryAssignment(models.Model):

    npa = models.ForeignKey(
        NPA,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    recovery_officer = models.ForeignKey(
        RecoveryOfficer,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    assigned_date = models.DateField()

    due_date = models.DateField(
        null=True,
        blank=True
    )

    assignment_status = models.CharField(
        max_length=34,
        choices=(
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('reassigned', 'Reassigned'),
        ),
        default='active'
    )

    remarks = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)