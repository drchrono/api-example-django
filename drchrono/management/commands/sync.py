from django.core.management.base import BaseCommand, CommandError
from drchrono.sync import sync_all


class Command(BaseCommand):
    help = 'Sync the local cache to the API'

    def handle(self, *args, **options):
        sync_all()