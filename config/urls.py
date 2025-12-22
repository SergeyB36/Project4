from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("users/", include("users.urls", namespace="users")),
    path("mail_messages/", include("mail_messages.urls", namespace="mail_messages")),
    # path("mail_recipients/", include("mail_recipients.urls", namespace="mail_recipients")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
