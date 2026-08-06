import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Oppretter (eller oppdaterer passordet til) Heine og Linnea sine kontoer."

    def handle(self, *args, **options):
        accounts = [
            ('heine', os.environ.get('HEINE_PASSWORD'), True),
            ('linnea', os.environ.get('LINNEA_PASSWORD'), False),
        ]

        for username, password, is_staff in accounts:
            if not password:
                self.stdout.write(self.style.WARNING(
                    f"Hopper over '{username}': ingen passord satt i miljøvariabel."
                ))
                continue

            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.is_staff = is_staff
            user.is_superuser = is_staff
            user.save()

            action = "Opprettet" if created else "Oppdaterte"
            self.stdout.write(self.style.SUCCESS(f"{action} bruker '{username}'."))
