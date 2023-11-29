from django.contrib import admin
from .models import Barangay, BusinessPermitApplication, BusinessBasicInformation, BusinessDetails, LessorDetails, BusinessActivity, BuildingPermitApplication, BuildingBasicInformation, BuildingDetails, BuildingOtherDetails, ApplicationRequirements, RequirementFiles, BuildingApplicationRequirements, BuildingRequirementFiles, Thread, Message, BuildingRequirementsChecklist, Appointment, AppointmentLimit, Soa, Department, BusinessDeptAssessment, BuildingDeptAssessment, Bill, BillFees, MessageAttachment, BankTransaction, LandbankTransaction, Faq, BusinessPermitFile, MobileBuild, MobileDownload, PisoPayTransaction
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from core.models import User, MyUserAdminForm
# Register your models here.


class MyUserAdmin(UserAdmin):
    form = MyUserAdminForm

class BuildingDetailsSearchAdmin(ModelAdmin):
    search_fields = ['id', 'application_number__id']

class BuildingApplicationSearchAdmin(ModelAdmin):
    search_fields = ['id', 'series_number', 'reference_id']

class BusinessApplicationSearchAdmin(ModelAdmin):
    search_fields = ['id', 'account_number', 'businessbasicinformation__reference_number']

class AppointmentLimitSearchAdmin(ModelAdmin):
    search_fields = ['date']

class BusinessDeptAssessmentSearchAdmin(ModelAdmin):
    search_fields = ['business_application__id']


class MobileBuildSearchAdmin(ModelAdmin):
    search_fields = ['is_active', 'for_maintenance', 'version']

admin.site.register(Barangay)
admin.site.register(BusinessPermitApplication, BusinessApplicationSearchAdmin)
admin.site.register(BusinessBasicInformation)
admin.site.register(BusinessDetails)
admin.site.register(LessorDetails)
admin.site.register(BusinessActivity)
admin.site.register(BuildingPermitApplication, BuildingApplicationSearchAdmin)
admin.site.register(BuildingBasicInformation, BuildingDetailsSearchAdmin)
admin.site.register(BuildingDetails, BuildingDetailsSearchAdmin)
admin.site.register(BuildingOtherDetails)
admin.site.register(ApplicationRequirements)
admin.site.register(RequirementFiles)
admin.site.register(BuildingApplicationRequirements)
admin.site.register(BuildingRequirementFiles)
admin.site.register(User, UserAdmin)
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(BuildingRequirementsChecklist)
admin.site.register(Appointment)
admin.site.register(AppointmentLimit, AppointmentLimitSearchAdmin)
admin.site.register(Soa)
admin.site.register(Department)
admin.site.register(BusinessDeptAssessment, BusinessDeptAssessmentSearchAdmin)
admin.site.register(BuildingDeptAssessment)
admin.site.register(Bill)
admin.site.register(BillFees)
admin.site.register(MessageAttachment)
admin.site.register(BankTransaction)
admin.site.register(LandbankTransaction)
admin.site.register(Faq)
admin.site.register(BusinessPermitFile)
admin.site.register(MobileBuild, MobileBuildSearchAdmin)
admin.site.register(MobileDownload)
admin.site.register(PisoPayTransaction)
UserAdmin.fieldsets += ('Custom fields set', {
    'fields': ('phone_number', 'department')
}),
