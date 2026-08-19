from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

class RecoveryOfficer(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='recovery_officer',
        null=True,
        blank=True
    )

    employee_id = models.CharField(
        max_length=20,
        unique = True
    )

    first_name = models.CharField(
        max_length=45
    )

    last_name = models.CharField(
        max_length=45
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    designation = models.CharField(
        max_length=45
    )

    region = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=45,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"