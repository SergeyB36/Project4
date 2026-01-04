from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mail_messages.apps import MailMessagesConfig
from mail_messages.views import (
    EmailMessageCreateView,
    EmailMessageDeleteView,
    EmailMessageDetailView,
    EmailMessageListView,
    EmailMessageUpdateView,
    HomeView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingUpdateView,
    post_mail,
)

app_name = MailMessagesConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("create_email/", EmailMessageCreateView.as_view(), name="create_email"),
    path("list_email/", EmailMessageListView.as_view(), name="list_email"),
    path("update_email/<int:pk>/", EmailMessageUpdateView.as_view(), name="update_email"),
    path("detail_email/<int:pk>/", EmailMessageDetailView.as_view(), name="detail_email"),
    path("confirm_delete_message/<int:pk>/", EmailMessageDeleteView.as_view(), name="confirm_delete_message"),
    path("create_mailing/", MailingCreateView.as_view(), name="create_mailing"),
    path("list_mailing/", MailingListView.as_view(), name="list_mailing"),
    path("detail_mailing/<int:pk>/", MailingDetailView.as_view(), name="detail_mailing"),
    path("update_mailing/<int:pk>/", MailingUpdateView.as_view(), name="update_mailing"),
    path("confirm_delete_mailing/<int:pk>/", MailingDeleteView.as_view(), name="confirm_delete_mailing"),
    path("mail_messages/<int:pk>/send", post_mail, name="send_mailing"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
