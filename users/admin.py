from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    list_filter = ("username",)
    search_fields = ("id", "username", "email")
