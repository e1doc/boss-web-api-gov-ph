from django.core.management.base import BaseCommand, CommandError
from api.models import BuildingPermitApplication
from datetime import datetime
from sequences import get_next_value
from services.series import SeriesService
class Command(BaseCommand):
    def handle(self, *args, **options):
        series = SeriesService()
        series.reset_series('rpt')
        self.stdout.write(self.style.SUCCESS('Series number reset successfully!'))
    
        
