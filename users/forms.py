# from django.contrib.auth.forms import UserCreationForm
#
# from users.models import CustomUser
#
#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ["avatar", "username", "email", "phone_number", "country", "password1", "password2"]
#
#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#
#         self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Имя пользователя"})
#         self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Адрес электронной почты"})
#         self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Пароль"})
#         self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Подтверждение пароля"})
