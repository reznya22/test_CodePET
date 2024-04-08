from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_to_email(message, recipient_list):
    """calling when user create collect or payment"""
    return send_mail(
            subject='CodePet',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_list, ]
        )
