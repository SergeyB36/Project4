from django.db import models
from django.db.models import Count, Q, ForeignKey
from django.utils import timezone

from mail_recipients.models import CustomMailRecipient
from users.models import CustomUser


class CustomMessage(models.Model):
    theme_mail = models.CharField(max_length=50, blank=True, null=True, verbose_name="Тема письма")
    text_mail = models.TextField(blank=False, null=False, verbose_name="Текст письма")
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Создатель сообщения",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="custom_messages",
    )


    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        unique_together = [('theme_mail', 'owner'), ]
        permissions = [
            ("can_view_message", "Can view message"),
        ]



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

    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Менеджер клиента рассылки",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="mailing",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        unique_together = [('message', 'owner'), ]
        permissions = [
            ("can_view_mailing", "Can view mailing"),
            ("can_moderated_mailing", "Can moderated mailing"),
        ]

    def update_status(self):
        now = timezone.now()

        for mailing in Mailing.objects.all():

            if not mailing.is_moderated:
                if mailing.start_time and mailing.end_time:
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

    @classmethod
    def get_user_stats(cls, user):
        """Возвращает статистику рассылок для пользователя"""
        return cls.objects.filter(owner=user).aggregate(
            count_on_moderation=Count('id', filter=Q(status="on_moderation")),
            count_created=Count('id', filter=Q(status="created")),
            count_completed=Count('id', filter=Q(status="completed")),
            count_started=Count('id', filter=Q(status="started")),
            count_failed=Count('id', filter=Q(status="failed")),
            total=Count('id'),
        )

class MailingAttempt(models.Model):
    recipients = models.ForeignKey( CustomMailRecipient, on_delete=models.CASCADE, related_name="mailing_recipients",)
    mailing = ForeignKey(
        Mailing,
        verbose_name="Рассылка",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="mailing",
    )
    STATUS_CHOICES = [('ok', 'Успешно'), ('failed', 'Ошибка')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус отправки")
    is_sending = models.BooleanField(null=True, blank=True)
    details = ''
    attempt_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Попытка отправки рассылки"
        verbose_name_plural = "Попытки отправки рассылок"
