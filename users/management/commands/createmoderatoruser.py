from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):

        group_name = "Moderator"
        group, created = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(
            codename__in=[
                "can_view_message",
                "can_moderated_mailing",
                "can_view_mailing",
                "can_view_recipient",
                "can_block_user",
                "can_view_user",
            ],
            content_type__app_label="users",
        )
        group.permissions.set(permissions)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана'))

        User = get_user_model()
        user, user_created = User.objects.get_or_create(
            email="usermoder@test.tt",
            username="Moderator",
            is_staff=False,
            is_superuser=False,
        )
        if user_created:
            user.set_password("1234")
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Пользователь с правами модератора успешно создан"))

        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(f'Пользователь "{user}" успешно добавлен в группу "{group}"'))
