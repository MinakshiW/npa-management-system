from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

class Customer(models.Model):

    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name='customer',
            null=True,
            blank=True
        )

    customer_code = models.CharField(
        max_length=20,
        unique=True
    )

    first_name = models.CharField(
        max_length=34
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

    address = models.TextField()

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=34,
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
        return self.first_name + " " + self.last_name