from django.db import models
from django.utils import timezone

from mail_recipients.models import CustomMailRecipient


class CustomMessage(models.Model):
    theme_mail = models.CharField(max_length=50, blank=True, null=True, verbose_name="Тема письма")
    text_mail = models.TextField(blank=False, null=False, verbose_name="Текст письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Сообщение. Тема: {self.theme_mail}"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('on_moderation', 'На модерации'),
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
        ('failed', 'Ошибка'),
    ]
    start_time = models.DateTimeField(blank=False, null=False, verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(blank=False, null=False, verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='on_moderation',
        verbose_name="Статус"
    )
    recipients = models.ManyToManyField(CustomMailRecipient, verbose_name="Получатели", related_name="mailing")
    message = models.ForeignKey(
        CustomMessage, on_delete=models.CASCADE, verbose_name="Сообщение", related_name="mailing"
    )
    is_moderated = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def update_status(self):
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
