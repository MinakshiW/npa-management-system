from django.db import models
from loan_app.models import Loan

NPA_CATEGORY_CHOICES = (
    ('substandard', 'Substandard'),
    ('doubtful', 'Doubtful'),
    ('loss', 'Loss Asset'),
)

RECOVERY_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('recovered', 'Recovered'),
    ('closed', 'Closed'),
)

class NPA(models.Model):

    loan = models.OneToOneField(
        Loan,
        on_delete=models.CASCADE,
        related_name='npa'
    )

    npa_date = models.DateField()

    days_past_due = models.PositiveIntegerField()

    npa_category = models.CharField(
        max_length=24,
        choices= NPA_CATEGORY_CHOICES,
        default='substandard'
    )

    recovery_status = models.CharField(
        max_length=34,
        choices= RECOVERY_STATUS_CHOICES,
        default='pending'
    )

    remarks = models.TextField(
        blank=True,
        null= True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.loan.loan_account_number


class NPAStatusHistory(models.Model):

    npa = models.ForeignKey(
        NPA,
        on_delete=models.CASCADE,
        related_name='status_history'
    )

    old_status = models.CharField(
        max_length=30
    )

    new_status = models.CharField(
        max_length=30
    )

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"NPA {self.npa.id}: {self.old_status} → {self.new_status}"