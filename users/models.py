from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=15, blank=True, null=True, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    avatar = models.ImageField(upload_to="users/image", blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна проживания")
    token = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email