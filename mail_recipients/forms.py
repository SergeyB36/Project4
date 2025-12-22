from django import forms
from django.core.validators import EmailValidator

from mail_recipients.models import CustomMailRecipient


class MailRecipientForm(forms.ModelForm):
    class Meta:
        model = CustomMailRecipient
        fields = ["email", "first_name", "last_name", "middle_name", "description"]
        email = forms.EmailField(validators=[EmailValidator()])

    def __init__(self, *args, **kwargs):
        super(MailRecipientForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "E-mail получателя"})
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Имя"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Фамилия"})
        self.fields["middle_name"].widget.attrs.update({"class": "form-control", "placeholder": "Отчество"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Комментарий"})
