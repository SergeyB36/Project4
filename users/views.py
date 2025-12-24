import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

# from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm, CustomUserModeratorForm, CustomUserUpdateForm
from users.models import CustomUser


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
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


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users:user_list")
    # включить после настройки прав доступа
    # def get_form_class(self):
    #     user = self.request.user
    #     if user == self.object.owner:
    #         return CustomUserCreationForm
    #     if user.groups.filter(name="Admin").exists():
    #         return CustomUserCreationForm
    #     if user.has_perm("catalog.can_unpublish_product"):
    #         return CustomUserModeratorForm
        # raise PermissionDenied("У вас недостаточно прав для редактирования этого товара")


class UserDetailView(DetailView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/user_detail.html"


class UserListView(ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    context_object_name = "objects_list"

class UserDeleteView(DeleteView):
    model = CustomUser
