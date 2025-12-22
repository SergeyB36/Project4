from django import forms

from mail_recipients.models import CustomMailRecipient


class MailRecipientForm(forms.ModelForm):
    class Meta:
        model = CustomMailRecipient
        fields = ["email", "first_name", "last_name", "middle_name", "description"]

    def __init__(self, *args, **kwargs):
        super(MailRecipientForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "E-mail получателя"})
