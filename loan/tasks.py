from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Loan
from users.models import AppUser

@shared_task
def send_loan_created_email(loan_id):
    try:
        loan = Loan.objects.get(pk=loan_id)
        user = loan.user
        send_mail(
            subject="Your loan request has been created",
            message=f"Dear {user.first_name}, your loan request for {loan.amount} has been received.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def assign_consultant_to_loan(loan_id):
    try:
        loan = Loan.objects.get(pk=loan_id)
        consultant = AppUser.objects.filter(role='CONSULTANT').order_by('?').first()
        if consultant:
            loan.consultant = consultant
            loan.save()
    except Loan.DoesNotExist:
        pass