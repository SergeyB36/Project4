from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from users.models import CustomUser


class CustomUserModeratorForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "is_active",
        ]


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
            'autocomplete': 'email'
        })
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["avatar", "username", "email", "phone_number", "country", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Иванов Иван Иванович"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Ivaniv@example.com"})
        self.fields["phone_number"].widget.attrs.update({"class": "form-control", "placeholder": "222-22-22"})
        self.fields["country"].widget.attrs.update({"class": "form-control", "placeholder": "Россия"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Подтверждение пароля"})


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["avatar", "username", "phone_number", "country"]

    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)

        self.fields["avatar"].widget.attrs.update(
            {"class": "form-control"},
        )
        self.fields["username"].widget.attrs.update(
            {"class": "form-control"},
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control"},
        )
        self.fields["country"].widget.attrs.update(
            {"class": "form-control"},
        )
