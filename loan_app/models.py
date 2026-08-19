from django.db import models
from customer_app.models import Customer

LOAN_TYPE_CHOICES = (
    ('home', 'Home Loan'),
    ('personal', 'Personal Loan'),
    ('education', 'Education Loan'),
    ('vehicle', 'Vehicle Loan'),
    ('gold', 'Gold Loan'),
    ('business', 'Business Loan'),
)

LOAN_STATUS_CHOICES = (
    ('active', 'Active'),
    ('closed', 'Closed'),
    ('npa', 'NPA'),
)

class Loan(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='loans'
    )

    loan_account_number = models.CharField(
        max_length=45,
        unique=True
    )

    loan_type = models.CharField(
        max_length=45,
        choices=LOAN_TYPE_CHOICES,
    )

    sanctioned_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    outstanding_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    emi_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tenure_months = models.PositiveIntegerField()

    sanction_date = models.DateField()

    loan_status = models.CharField(
        max_length=34,
        choices=LOAN_STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.loan_account_number