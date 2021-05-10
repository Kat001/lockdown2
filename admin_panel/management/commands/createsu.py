from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from Accounts.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Account.objects.filter(username="admin").exists():
            Account.objects.create_superuser(
                "admin", "admin")
            print("Created new superuser")
        else:
            print("Superuser already exists")
