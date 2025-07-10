from django.core.management.base import BaseCommand
from getpass import getpass
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from user.models import User


class Command(BaseCommand):
    help = 'Створити нового адміністратора через CLI'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=== Створення адміністратора ==='))

        # Email
        while True:
            email = input('Email: ').strip()
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    self.stdout.write(self.style.ERROR('❌ Такий email вже існує.'))
                    continue
                break
            except ValidationError:
                self.stdout.write(self.style.ERROR('❌ Некоректний email.'))

        # Ім'я
        while True:
            first_name = input("Ім'я: ").strip()
            if first_name:
                break
            self.stdout.write(self.style.ERROR('Імʼя не може бути порожнім.'))

        # Прізвище
        while True:
            last_name = input("Прізвище: ").strip()
            if last_name:
                break
            self.stdout.write(self.style.ERROR('Прізвище не може бути порожнім.'))

        # Пароль
        while True:
            password = getpass('Тимчасовий пароль: ')
            confirm_password = getpass('Повторіть пароль: ')
            if password != confirm_password:
                self.stdout.write(self.style.ERROR('❌ Паролі не збігаються.'))
            elif len(password) < 6:
                self.stdout.write(self.style.ERROR('❌ Пароль має бути щонайменше 6 символів.'))
            else:
                break

        # Створення користувача
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='admin',
            is_staff=True,
            is_superuser=True,
            must_change_password=True,
        )
        user.save()

        self.stdout.write(self.style.SUCCESS(f'✅ Адміністратор {email} створений.'))
    