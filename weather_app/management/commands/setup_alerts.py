from django.core.management.base import BaseCommand
from django.conf import settings
from weather_app.models import AlertConfig

class Command(BaseCommand):
    help = 'Set up initial alert configurations for all cities'

    def handle(self, *args, **kwargs):
        for city in settings.CITIES:
            AlertConfig.objects.get_or_create(
                city=city,
                defaults={
                    'max_temp': 35,
                    'min_temp': 10,
                    'condition': 'Rain'
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully set up alert configurations'))
        