import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

# from config.settings import EMAIL_HOST_USER
# from users.forms import CustomUserCreationForm
from users.models import CustomUser


class UserCreateView(CreateView):
    model = CustomUser
    # form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/new_user_create.html"

    # def form_valid(self, form):
    #     user = form.save()
    #     user.is_active = False
    #     token = secrets.token_hex(16)
    #     user.token = token
    #     user.save()
    #     host = self.request.get_host()
    #     url = f"http://{host}/users/email_confirm/{token}/"
    #     send_mail(
    #         subject="Подтверждение почты",
    #         message=f"Привет! Перейди по ссылке для завершения регистрации {url}",
    #         from_email=EMAIL_HOST_USER,
    #         recipient_list=[user.email],
    #     )
    #     return super().form_valid(form)


# def email_verification(request, token):
#     user = get_object_or_404(CustomUser, token=token)
#     user.is_active = True
#     user.token = None
#     user.save()
#     return redirect(reverse("users:login"))