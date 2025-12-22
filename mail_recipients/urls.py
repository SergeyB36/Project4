from django.conf import settings
from django.conf.urls.static import static

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
