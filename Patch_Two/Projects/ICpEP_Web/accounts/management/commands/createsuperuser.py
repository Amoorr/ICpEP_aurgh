from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Create a single superuser if one does not already exist'

    def handle(self, *args, **kwargs):
        if CustomUser.objects.filter(role='superuser').exists():
            self.stdout.write(self.style.WARNING('A superuser already exists.'))
            return

        email = input("Enter superuser email: ")
        password = input("Enter superuser password: ")

        superuser = CustomUser.objects.create_superuser(
            name=email,
            password=password,
            given_name='Super',
            last_name='User',
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully!"))
