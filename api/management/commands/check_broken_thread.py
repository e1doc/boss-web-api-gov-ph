from django.core.management.base import BaseCommand, CommandError
from api.models import Thread, BuildingPermitApplication
from sequences import get_next_value
from services.series import SeriesService
from api.serializers import InquiryListSerializer
from core.models import User
class Command(BaseCommand):
    def handle(self, *args, **options):
        threads = Thread.objects.filter(receiver__isnull=True, sender__is_staff = True, is_remarks=True).order_by('created_at')      
        serializer = InquiryListSerializer(threads, many=True)
        for item in serializer.data:
            if item['building_id'] is not None:
                thread = Thread.objects.get(id=item['id'])
                user = User.objects.get(id=item['building_id']['user'])
                thread.receiver = user
                thread.save()
            elif item['business_id'] is not None:
                thread = Thread.objects.get(id=item['id'])
                user = User.objects.get(id=item['business_id']['user'])
                thread.receiver = user
                thread.save()
        self.stdout.write(self.style.SUCCESS('Broken threads %d' % (len(threads))))
    
        
