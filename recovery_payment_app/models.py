from django.db import models
from npa_app.models import NPA

PAYMENT_MODE_CHOICES = (
    ('cash', 'Cash'),
    ('upi', 'UPI'),
    ('bank', 'Bank Transfer'),
    ('cheque', 'Cheque'),
    ('card', 'Card'),
)

class RecoverPayment(models.Model):

    npa = models.ForeignKey(
        NPA,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    payment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_date = models.DateField()

    payment_mode = models.CharField(
        max_length=34,
        choices= PAYMENT_MODE_CHOICES,
    )

    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Recovery Payment: {self.npa.loan.loan_account_number}"