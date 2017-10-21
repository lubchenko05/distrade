from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from distrade.local_settings import ADMIN_USERNAME, ADMIN_PASSWORD


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            admin = get_user_model().objects.create_superuser(username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        except:
            pass