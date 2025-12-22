from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from mail_recipients.forms import MailRecipientForm
from mail_recipients.models import CustomMailRecipient


class MailRecipientCreateView(CreateView):
    model = CustomMailRecipient
    form_class = MailRecipientForm
    template_name = "mail_recipients/create_mail_recipient.html"
    success_url = reverse_lazy("mail_recipients:list_mail_recipient")


class MailRecipientListView(ListView):
    model = CustomMailRecipient
    template_name = "mail_recipients/list_mail_recipient.html"
    context_object_name = "objects_list"


class MailRecipientDetailView(DetailView):
    model = CustomMailRecipient
    form_class = MailRecipientForm
    template_name = "mail_recipients/detail_mail_recipient.html"


class MailRecipientDeleteView(DeleteView):
    model = CustomMailRecipient
    template_name = "mail_recipients/confirm_delete_recipient.html"
    success_url = reverse_lazy("mail_recipients:list_mail_recipient")


class MailRecipientUpdateView(UpdateView):
    model = CustomMailRecipient
    form_class = MailRecipientForm
    template_name = "mail_recipients/update_mail_recipient.html"
    success_url = reverse_lazy("mail_recipients:list_mail_recipient")
