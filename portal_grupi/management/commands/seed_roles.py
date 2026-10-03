from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from portal_grupi.models import Profile


class Command(BaseCommand):
    help = 'Створює базові ролі та демонстраційних адміністраторів.'

    def handle(self, *args, **options):
        roles = ['user', 'moderator', 'admin']
        for role in roles:
            Group.objects.get_or_create(name=role)
            self.stdout.write(self.style.SUCCESS(f'Роль готова: {role}'))

        admin_users = [
            ('teacher', 'teacher@example.com', 'teacher123', 'Викладач'),
            ('project_manager', 'manager@example.com', 'manager123', 'Керівник проекту'),
        ]

        for username, email, password, full_name in admin_users:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            if created:
                user.set_password(password)
            user.is_staff = True
            user.is_superuser = False
            user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = 'admin'
            profile.full_name = full_name
            profile.save()

            self.stdout.write(self.style.SUCCESS(f'Адміністратор готовий: {username}'))

        self.stdout.write(self.style.SUCCESS('Базові ролі та адміністратори створені.'))
