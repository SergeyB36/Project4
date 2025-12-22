from django.contrib import admin

from mail_messages.models import Mailing, CustomMessage



@admin.register(CustomMessage)
class CustomMessageAdmin(admin.ModelAdmin):
    list_display = ("theme_mail", "text_mail")
    list_filter = ("theme_mail", "text_mail")
    search_fields = ("theme_mail", "text_mail")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "start_time", "end_time", "message", "is_moderated")
    list_filter = ("message", "status", "recipients")
    search_fields = ("status", "recipients", "message",)
