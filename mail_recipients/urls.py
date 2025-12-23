from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mail_recipients.apps import MailRecipientsConfig
from mail_recipients.views import MailRecipientCreateView, MailRecipientListView, MailRecipientDetailView, \
    MailRecipientDeleteView, MailRecipientUpdateView

app_name = MailRecipientsConfig.name

urlpatterns = [
    path("create_mail_recipient/", MailRecipientCreateView.as_view(), name="create_mail_recipient"),
    path("list_mail_recipient/", MailRecipientListView.as_view(), name="list_mail_recipient"),
    path("detail_mail_recipient/<int:pk>/", MailRecipientDetailView.as_view(), name="detail_mail_recipient"),
    path("confirm_delete_recipient/<int:pk>/", MailRecipientDeleteView.as_view(), name="confirm_delete_recipient"),
    path("update_mail_recipient/<int:pk>/", MailRecipientUpdateView.as_view(), name="update_mail_recipient"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
