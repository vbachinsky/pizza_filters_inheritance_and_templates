# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from core.email_service import EmailService

class AccountsEmailService(EmailService):

    ADMIN_EMAILS = []
    USER_EMAILS = []

    @staticmethod
    def send_forgot_password(reset_data):
        to_email = [reset_data.user.email]
        # if settings.DEBUG:
            # to_email = EmailService.USER_EMAILS

        email_content = get_template('emails/forgot_password_email.html')
        context = {
            'reset_data': reset_data,
            'domain': settings.SITE_URL
        }

        html_content = email_content.render(context)
        subject = 'Reset password request'

        msg = EmailMultiAlternatives(subject, html_content, settings.NO_REPLY_EMAIL_ADDRESS, to_email)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @staticmethod
    def send_registration_email(user):
        to_email = [user.email]

        email_content = get_template('emails/registration_email.html')
        context = {
            'user': user,
            'domain': settings.SITE_URL
        }

        html_content = email_content.render(context)
        subject = 'Confirm Registration'

        msg = EmailMultiAlternatives(subject, html_content, settings.NO_REPLY_EMAIL_ADDRESS, to_email)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

