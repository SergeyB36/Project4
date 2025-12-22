# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group, Permission
# from django.core.management.base import BaseCommand
#
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#
#         group_name = "Модератор продуктов"
#         group, created = Group.objects.get_or_create(name=group_name)
#         permissions = Permission.objects.filter(
#             codename__in=[
#                 "can_unpublish_product",
#                 "delete_product",
#             ],
#             content_type__app_label="catalog",
#         )
#         group.permissions.set(permissions)
#         if created:
#             self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана'))
#         else:
#             self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" уже была создана'))
#         User = get_user_model()
#         user = User.objects.create(
#             email="moderatoruser@test.tt",
#             first_name="Moderator",
#             last_name="Products",
#             is_staff=False,
#             is_superuser=False,
#         )
#
#         user.set_password("1234")
#         user.is_active = True
#
#         user.save()
#
#         self.stdout.write(self.style.SUCCESS(f"Пользователь с правами модератора продуктов успешно создан"))
#
#         user.groups.add(group)
#
#         self.stdout.write(self.style.SUCCESS(f'Пользователь "{user}" успешно добавлен в группу "{group}"'))
