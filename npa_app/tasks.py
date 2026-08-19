# npa_app/tasks.py

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from recovery_assignement_app.models import RecoveryAssignment


@shared_task
def send_overdue_npa_reminders():

    today = timezone.localdate()

    assignments = RecoveryAssignment.objects.select_related(
        'npa__loan',
        'recovery_officer__user'
    ).filter(
        assignment_status='active',
        due_date__lt=today,
        npa__recovery_status='in_progress'
    )

    for assignment in assignments:

        officer = assignment.recovery_officer

        send_mail(
            subject='Overdue NPA Recovery Reminder',
            message=f"""
Hello {officer.first_name},

The following NPA recovery assignment is overdue.

Loan Account:
{assignment.npa.loan.loan_account_number}

Due Date:
{assignment.due_date}

Please take the necessary action.

NPA Management System
""",
            from_email=None,
            recipient_list=[officer.email],
            fail_silently=False
        )

    return f"{assignments.count()} overdue NPA reminders processed."