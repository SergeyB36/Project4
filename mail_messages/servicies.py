from smtplib import SMTPException
from time import timezone

from django.conf import settings
from django.core.mail import send_mail

from mail_messages.models import Mailing, MailingAttempt


def send_mailing(mailing:Mailing) -> None:
    mailing.start_at = timezone.now()
    mailing.save()

    recipients = mailing.recipients.all()
    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.theme_mail,
                message=mailing.message.text_mail,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient.email],
            )
        except SMTPException as e:
            MailingAttempt.objects.create(mailing=Mailing, recipient=recipient, status="failed", detail=str(e), is_sending=False)
        else:
            MailingAttempt.objects.create(mailing=Mailing, recipient=recipient, status="ok", is_sending=True)