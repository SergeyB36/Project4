from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views

from users.apps import UsersConfig

from users.views import UserCreateView, UserDetailView, UserUpdateView, UserListView, \
    UserDeleteView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("email_confirm/<str:token>/", email_verification, name="email_confirm"),
    path("new_user_create/", UserCreateView.as_view(template_name="users/new_user_create.html"), name="new_user_create"),
    path("user_detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user_update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_confirm_delete/<int:pk>/", UserDeleteView.as_view(), name="user_confirm_delete"),
    # path("change-password/", auth_views.PasswordChangeView.as_view(template_name="change-password.html"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
