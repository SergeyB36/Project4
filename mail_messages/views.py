from django.contrib.auth.mixins import LoginRequiredMixin
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


class EmailMessageCreateView(LoginRequiredMixin, CreateView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/create_email.html"
    success_url = reverse_lazy("mail_messages:list_email")

    def form_valid(self, form):
        mail_message = form.save()
        owner = self.request.user
        mail_message.owner = owner
        mail_message.save()
        form.save()
        return super().form_valid(form)


class EmailMessageDetailView(LoginRequiredMixin, DetailView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/detail_email.html"


class EmailMessageListView(LoginRequiredMixin, ListView):
    model = CustomMessage
    template_name = "mail_messages/list_email.html"
    context_object_name = "objects_list"


class EmailMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/update_email.html"
    success_url = reverse_lazy("mail_messages:list_email")


class EmailMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomMessage
    template_name = "mail_messages/confirm_delete_message.html"
    success_url = reverse_lazy("mail_messages:list_email")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/create_mailing.html"
    success_url = reverse_lazy("mail_messages:list_mailing")

    def form_valid(self, form):
        mail_mailing = form.save()
        owner = self.request.user
        mail_mailing.owner = owner
        mail_mailing.save()
        form.save()
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mail_messages/list_mailing.html"
    context_object_name = "objects_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for mailing in context['object_list']:
            mailing.update_status()
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/detail_mailing.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/update_mailing.html"
    success_url = reverse_lazy("mail_messages:list_mailing")


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mail_messages/confirm_delete_mailing.html"
    success_url = reverse_lazy("mail_messages:list_mailing")
