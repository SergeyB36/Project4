from django.conf import settings
from django.conf.urls.static import static

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
