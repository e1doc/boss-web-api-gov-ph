from django.core.management.base import BaseCommand, CommandError
from api.models import BuildingPermitApplication
from api.serializers import BuildingApplicationListSerializer
class Command(BaseCommand):
    def handle(self, *args, **options):
        affected_count = 0
        reference_ids = ''
        applications = BuildingPermitApplication.objects.order_by('created_at')
        serializer = BuildingApplicationListSerializer(
            applications, many=True)
        for application in serializer.data:
            if application['buildingdetails'] is None and application['is_enrolled']:
                affected_count += 1
                reference_ids = '%s, %s: %s' % (reference_ids, application['id'], application['reference_id'])
        self.stdout.write(self.style.SUCCESS(affected_count))
        self.stdout.write(self.style.SUCCESS(reference_ids))
    
        
