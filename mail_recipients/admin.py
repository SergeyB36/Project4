from django.contrib import admin

from mail_recipients.models import CustomMailRecipient


@admin.register(CustomMailRecipient)
class CustomMailRecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "middle_name", "owner", "description")
    list_filter = ("last_name", "email")
    search_fields = ("email", "first_name", "last_name", "middle_name", "owner", "description")
