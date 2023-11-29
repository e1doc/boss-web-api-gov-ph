from django.core.management.base import BaseCommand, CommandError
from api.models import BuildingPermitApplication
from datetime import datetime
from sequences import get_next_value
from services.series import SeriesService
class Command(BaseCommand):
    def handle(self, *args, **options):
        applications = BuildingPermitApplication.objects.order_by('created_at')
        for application in applications:
            series = SeriesService(application=application)
            application.series_number = series.generate_series()
            application.save()
        self.stdout.write(self.style.SUCCESS('Series number updated successfully!'))
    
        
