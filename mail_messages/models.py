from django.db import models

from mail_recipients.models import CustomMailRecipient


class CustomMessage(models.Model):
    theme_mail = models.CharField(max_length=50, blank=True, null=True, verbose_name="Тема письма")
    text_mail = models.TextField(blank=False, null=False, verbose_name="Текст письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщений"

    def __str__(self):
        return f"Сообщение. Тема: {self.theme_mail}"


class Mailing(models.Model):
    stat_time = models.DateTimeField(blank=False, null=False, verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(blank=False, null=False, verbose_name="Дата и время окончания отправки")
    status = models.Choices
    recipients = models.ManyToManyField(CustomMailRecipient, verbose_name="Получатели", related_name="mailings")
    message = models.ForeignKey(
        CustomMessage, on_delete=models.CASCADE, verbose_name="Сообщение", related_name="mailing"
    )
