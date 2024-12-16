from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a Django superuser with a specified password (non-interactive)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username", required=True, help="Username for the superuser"
        )
        parser.add_argument(
            "--email", required=True, help="Email address for the superuser"
        )
        parser.add_argument(
            "--password", required=True, help="Password for the superuser"
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        email = kwargs["email"]
        password = kwargs["password"]

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"Superuser '{username}' already exists.")
            )
        else:
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' created successfully.")
            )
