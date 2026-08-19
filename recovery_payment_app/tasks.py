from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from recovery_assignement_app.models import RecoveryAssignment

from .models import RecoverPayment


@shared_task(bind=True,
            autoretry_for=(Exception,),
            retry_backoff=True,
            max_retries = 3
             )
def send_payment_notification(payment_id):

    try:
        payment = RecoverPayment.objects.select_related(
            'npa__loan__customer'
        ).get(id=payment_id)

        customer = payment.npa.loan.customer
        loan = payment.npa.loan

        print("CUSTOMER:", customer.first_name)
        print("CUSTOMER EMAIL:", customer.email)

        subject = "Recovery Payment Received"

        message = f"""
                        Hello {customer.first_name},

                        We have successfully received your recovery payment.

                        Loan Account: {loan.loan_account_number}    
                        Payment Amount: ₹{payment.payment_amount}
                        Payment Date: {payment.payment_date}
                        Remaining Outstanding Amount: ₹{loan.outstanding_amount}

                        Thank you.

                        NPA Management System
                    """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[customer.email],
            fail_silently=False
        )

        return f"Payment notification sent for payment {payment_id}"

    except RecoverPayment.DoesNotExist:

        return f"Payment {payment_id} does not exist."

