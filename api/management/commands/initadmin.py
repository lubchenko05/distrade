from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            admin = get_user_model().objects.create_superuser(username='username', password='password')
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        except:
            pass