from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(subject, recipient, template_name, context):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    try:
        send_mail(subject=subject,
                  message=plain_message,
                  html_message=html_message,
                  from_email=from_email,
                  recipient_list=[recipient])
    except SMTPException:
        print("Failed to send mail.")
