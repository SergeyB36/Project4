from django import forms
from django.utils import timezone

from mail_messages.models import CustomMessage, Mailing


# from mail_messages.servicies import update_status


class MailMessagesForm(forms.ModelForm):

    class Meta:
        model = CustomMessage
        fields = ["theme_mail", "text_mail"]

    def __init__(self, *args, **kwargs):
        super(MailMessagesForm, self).__init__(*args, **kwargs)

        self.fields["theme_mail"].widget.attrs.update(
            {"class": "form-control"},
        )
        self.fields["text_mail"].widget.attrs.update(
            {"class": "form-control"},
        )

    def clean_theme_mail(self):
        cleaned_data = super().clean()
        theme_mail = cleaned_data.get("theme_mail")
        theme_mail_error = [
            "спам",
        ]
        if theme_mail in theme_mail_error:
            self.add_error("theme_mail", f"Тема не может содержать слово {theme_mail}")
        if len(theme_mail) > 50:
            self.add_error("theme_mail", "Количество символов в теме не должно быть больше 50")
        return theme_mail

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "recipients", "message", "status"]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'recipients': forms.CheckboxSelectMultiple(),
            'message': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

    #
    # def changed_data(self):
    #     cleaned_data = super().clean()
    #     start_time = cleaned_data.get('start_time')
    #     end_time = cleaned_data.get('end_time')
    #
    #     if start_time < timezone.now():
    #         self.add_error('start_time', 'Дата начала не может быть в прошлом')
