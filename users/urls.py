from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig

from users.views import UserCreateView#, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path(
        "new_user_create/", UserCreateView.as_view(template_name="users/new_user_create.html"), name="new_user_create"
    ),
#     path("email_confirm/<str:token>", email_verification, name="email_confirm"),
#     path(
#         "new_user_create/", UserCreateView.as_view(template_name="users/new_user_create.html"), name="new_user_create"
#     ),
#     path("email_confirm/<str:token>/", email_verification, name="email_confirm"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
