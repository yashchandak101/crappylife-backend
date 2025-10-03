from django.core.mail import send_mail
from django.conf import settings

def send_newsletter(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER if hasattr(settings, "EMAIL_HOST_USER") else "admin@example.com",
        recipient_list,
        fail_silently=False,   # ⚠ Important for debugging
    )
