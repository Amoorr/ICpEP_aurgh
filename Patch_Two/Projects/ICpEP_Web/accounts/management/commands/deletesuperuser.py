from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Delete the superuser account'

    def handle(self, *args, **kwargs):
        superuser = CustomUser.objects.filter(role='superuser').first()
        if superuser:
            confirmation = input(f"Are you sure you want to delete superuser {superuser.email}? (yes/no): ")
            if confirmation.lower() == 'yes':
                superuser.delete()
                self.stdout.write(self.style.SUCCESS('Superuser deleted successfully!'))
            else:
                self.stdout.write(self.style.WARNING('Superuser deletion cancelled.'))
        else:
            self.stdout.write(self.style.ERROR('No superuser exists.'))
