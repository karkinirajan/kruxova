from django.core.management.base import BaseCommand
from apps.main.models import Data, Indicator


class Command(BaseCommand):
    help = "Match indicators to datasources"

    def handle(self, *args, **options):
        # Get all indicators
        indicators = Indicator.objects.all()
        for indicator in indicators:
            # Get the data for the indicator
            data = Data.objects.filter(indicator=indicator)

            for d in data:
                indicator.datasources.add(d.datasource)
                message = f"Added datasource {d.datasource.name} to indicator {indicator.name}"
                self.stdout.write(self.style.SUCCESS(message))
