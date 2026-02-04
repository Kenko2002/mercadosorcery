import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Creates a superuser from environment variables non-interactively"

    def handle(self, *args, **options):
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([email, password]):
            self.stdout.write(self.style.ERROR(
                'Missing environment variables: DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD'
            ))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.SUCCESS(f'Superuser with email \"{email}\" already exists.'))
        else:
            # When using a custom user model with email as USERNAME_FIELD,
            # create_superuser expects the email to be passed as the username.
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser \"{email}\".'))
