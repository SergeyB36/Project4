from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from mail_messages.forms import MailMessagesForm, MailingForm
from mail_messages.models import CustomMessage, Mailing


class HomeView(TemplateView):
    template_name = "mail_messages/home.html"


class EmailMessageCreateView(CreateView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/create_email.html"
    success_url = reverse_lazy("mail_messages:list_email")


class EmailMessageDetailView(DetailView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/detail_email.html"


class EmailMessageListView(ListView):
    model = CustomMessage
    template_name = "mail_messages/list_email.html"
    context_object_name = "objects_list"


class EmailMessageUpdateView(UpdateView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/update_email.html"
    success_url = reverse_lazy("mail_messages:list_email")


class EmailMessageDeleteView(DeleteView):
    model = CustomMessage
    template_name = "mail_messages/confirm_delete_message.html"
    success_url = reverse_lazy("mail_messages:list_email")


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/create_mailing.html"
    success_url = reverse_lazy("mail_messages:list_mailing")


class MailingListView(ListView):
    model = Mailing
    template_name = "mail_messages/list_mailing.html"
    context_object_name = "objects_list"


class MailingDetailView(DetailView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/detail_mailing.html"


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/update_mailing.html"
    success_url = reverse_lazy("mail_messages:list_mailing")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mail_messages/confirm_delete_mailing.html"
    success_url = reverse_lazy("mail_messages:list_mailing")
