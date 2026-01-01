from django.db import models

from users.models import CustomUser


class CustomMailRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    first_name = models.CharField(max_length=50, blank=False, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=False, null=True, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=False, null=True, verbose_name="Отчество")
    description = models.TextField(blank=False, verbose_name="Комментарий")
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Менеджер клиента рассылки",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="mail_recipient",
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        unique_together = [
            ("email", "owner"),
        ]
        permissions = [
            ("can_view_recipient", "Can view recipient"),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
