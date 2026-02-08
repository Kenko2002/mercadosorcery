import os
from django.core.management.base import BaseCommand
from socialentities.models import SocialEntity

class Command(BaseCommand):
    """
    Create a superuser if one does not exist.
    This command is idempotent and safe to run on every deployment.
    It uses the following environment variables:
    - DJANGO_SUPERUSER_USERNAME
    - DJANGO_SUPERUSER_EMAIL
    - DJANGO_SUPERUSER_PASSWORD
    """
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.WARNING('Missing superuser environment variables. Skipping creation.'))
            return

        if not SocialEntity.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Creating superuser: {username}'))
            SocialEntity.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists.'))
