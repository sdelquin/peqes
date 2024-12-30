from django.core.management.base import BaseCommand
from django.utils import timezone

from joints.models import Joint


class Command(BaseCommand):
    help = 'Delete expired joints'

    def handle(self, *args, **options):
        Joint.objects.filter(expires_at__lte=timezone.now()).delete()
