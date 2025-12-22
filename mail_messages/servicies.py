from django.utils import timezone

from mail_messages.models import Mailing


def update_status():
    now = timezone.now()

    for mailing in Mailing.objects.all():

        if not mailing.is_moderated:
            mailing.status = "on_moderation"

        elif mailing.start_time and mailing.end_time:
            if now < mailing.start_time:
                mailing.status = "created"
            elif mailing.start_time <= now <= mailing.end_time:
                mailing.status = "started"
            elif now > mailing.end_time:
                mailing.status = "completed"
            else:
                mailing.status = "failed"
        else:
            mailing.status = "failed"

        mailing.save()

    return True