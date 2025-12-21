from django import forms

from mail_messages.models import CustomMessage


class MailMessagesForm(forms.ModelForm):
    class Meta:
        model = CustomMessage
        fields = ["theme_mail", "text_mail"]