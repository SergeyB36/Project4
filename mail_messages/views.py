from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from mail_messages.forms import MailingForm, MailingModeratorForm, MailMessagesForm
from mail_messages.models import CustomMessage, Mailing, MailingAttempt
from mail_messages.servicies import send_mailing
from mail_recipients.models import CustomMailRecipient


class CustomMailing:
    pass


class HomeView(TemplateView):
    template_name = "mail_messages/home.html"

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_authenticated and not user.groups.filter(name="Moderator").exists():
            return queryset.filter(owner=user)
        if user.groups.filter(name="Moderator").exists():
            return queryset
        return self.model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated:
            return context
        if user.is_authenticated and not user.groups.filter(name="Moderator").exists():
            context = super().get_context_data(**kwargs)
            context["messages"] = MailingAttempt.objects.filter(mailing__owner=user).aggregate(
                ok_cnt=Count("id", filter=Q(status="ok")),
                failed_cnt=Count("id", filter=Q(status="failed")),
            )
            context["recipients"] = CustomMailRecipient.objects.filter(owner=user).aggregate(
                count=Count("id"),
            )
            context["mailing_stats"] = Mailing.get_user_stats(self.request.user)
        if user.is_authenticated and user.groups.filter(name="Moderator").exists():
            return context
        else:
            return context


class EmailMessageCreateView(LoginRequiredMixin, CreateView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/create_email.html"
    success_url = reverse_lazy("mail_messages:list_email")

    def form_valid(self, form):
        mail_message = form.save()
        owner = self.request.user
        mail_message.owner = owner
        cache.delete(f"user_{self.request.user.id}_messages")
        return super().form_valid(form)


class EmailMessageDetailView(LoginRequiredMixin, DetailView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/detail_email.html"

    def get_object(self, queryset=None):
        cache_key = f'mail_message_{self.kwargs["pk"]}'
        obj = cache.get(cache_key)
        if obj is None:
            obj = super().get_object(queryset)
            if hasattr(obj, "update_status"):
                obj.update_status()
            cache.set(cache_key, obj)
        return obj


class EmailMessageListView(LoginRequiredMixin, ListView):
    model = CustomMessage
    template_name = "mail_messages/list_email.html"
    context_object_name = "objects_list"

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_authenticated and not user.groups.filter(name="Moderator").exists():
            return queryset.filter(owner=user)
        if user.groups.filter(name="Moderator").exists():
            return queryset
        return self.model.objects.none()


class EmailMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomMessage
    form_class = MailMessagesForm
    template_name = "mail_messages/update_email.html"
    success_url = reverse_lazy("mail_messages:list_email")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f"mail_message_{self.object.pk}")
        cache.delete(f"user_{self.request.user.id}_messages")
        return response


class EmailMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomMessage
    template_name = "mail_messages/confirm_delete_message.html"
    success_url = reverse_lazy("mail_messages:list_email")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = self.object.pk
        user_id = request.user.id

        response = super().delete(request, *args, **kwargs)

        cache.delete(f"mail_message_{pk}")
        cache.delete(f"user_{user_id}_messages")

        return response


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/create_mailing.html"
    success_url = reverse_lazy("mail_messages:list_mailing")

    def form_valid(self, form):
        mail_mailing = form.save()
        mail_mailing.owner = self.request.user
        mail_mailing.save()
        cache.delete(f"user_{self.request.user.id}_messages")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mail_messages/list_mailing.html"
    context_object_name = "objects_list"

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_authenticated and not user.groups.filter(name="Moderator").exists():
            return queryset.filter(owner=user)
        if user.groups.filter(name="Moderator").exists():
            return queryset
        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for mailing in context["object_list"]:
            mailing.update_status()
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/detail_mailing.html"

    def get_object(self, queryset=None):
        cache_key = f'mailing_{self.kwargs["pk"]}'
        if cache.get(cache_key):
            obj = cache.get(cache_key)
        obj = super().get_object(queryset)
        obj.update_status()
        cache.set(obj, cache_key)
        return obj


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mail_messages/update_mailing.html"
    success_url = reverse_lazy("mail_messages:detail_mailing")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if user.groups.filter(name="Moderator").exists():
            return MailingModeratorForm
        return MailingForm

    def form_valid(self, form):
        mail_mailing = form.save()
        mail_mailing.is_moderated = False
        mail_mailing.update_status()
        mail_mailing.save()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user

        if user.groups.filter(name="Moderator").exists():
            return reverse_lazy("mail_messages:list_mailing")

        return reverse_lazy("mail_messages:detail_mailing", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        """Определяем, какие объекты видны"""
        user = self.request.user

        if user.groups.filter(name="Moderator").exists():
            return Mailing.objects.all()

        return Mailing.objects.filter(owner=user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mail_messages/confirm_delete_mailing.html"
    success_url = reverse_lazy("mail_messages:list_mailing")


def post_mail(pk):
    """POST запрос - создаем и отправляем рассылку"""

    try:
        mailing = get_object_or_404(Mailing, pk=pk)
        send_mailing(pk)
        mailing.status = "completed"
        mailing.end_time = timezone.now()
        mailing.save()
        return redirect("mail_messages:home")
    except Exception:
        return redirect("mail_messages:home")
