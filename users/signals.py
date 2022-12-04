from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User
from utils.mail_service import send_email
from .tokens import account_activation_token


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        context = {
            "username": instance.username,
            "domain": "127.0.0.1:8000/",
            "uid": urlsafe_base64_encode(force_bytes(instance.id)),
            "token": account_activation_token.make_token(instance)
        }
        send_email("Welcome to Fresh Shop", instance.email, "email/welcome.html", context)
