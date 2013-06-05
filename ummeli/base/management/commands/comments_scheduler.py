from django.core.management.base import BaseCommand
from ummeli.vlive.tasks import *


class Command(BaseCommand):
    help = 'Enable/Disable commenting on articles'

    def handle(self, **options):
        disable_comments_scheduler()
