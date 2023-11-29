from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from api.custom_storage import PrivateMediaStorage
from pprint import pprint
import string
import random
import uuid
# Create your models here.


class Barangay(models.Model):
    name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BusinessPermitApplication(models.Model):

    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, blank=True)
    application_status = models.IntegerField(default=0)
    is_draft = models.BooleanField(default=True, blank=True)
    is_approve = models.BooleanField(default=False)
    is_disapprove = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    date_renewed = models.DateTimeField(null=True, blank=True)
    is_enrolled = models.BooleanField(default=False)
    last_submitted = models.DateTimeField(null=True, blank=True)
    latest_approver = models.ForeignKey('api.Department', on_delete= models.SET_NULL, null=True, blank=True)
    application_type = models.CharField(max_length=20, default='new')
    is_renewed = models.BooleanField(default=False)
    on_renewal = models.BooleanField(default=False)
    last_renewal = models.DateTimeField(null=True, blank=True)
    latest_approval_date = models.DateTimeField(null=True, blank=True)
    is_renewal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['created_at']


class BusinessBasicInformation(models.Model):
    application_number = models.OneToOneField(
        BusinessPermitApplication,
        on_delete=models.CASCADE,
    )

    dti_sec_cda_reg_number = models.CharField(max_length=50,
                                              blank=True,
                                              default="")
    dti_sec_cda_reg_date = models.DateTimeField(null=True, blank=True)
    type_of_organization = models.CharField(max_length=20, blank=True)
    ctc_no = models.CharField(max_length=20, blank=True)
    tin = models.CharField(max_length=20, blank=True)
    has_tax_incentive = models.BooleanField(default=False, blank=True)
    government_entity = models.CharField(max_length=50, blank=True)

    reference_number = models.CharField(max_length=20, blank=True)
    owner_first_name = models.CharField(max_length=50, blank=True)
    owner_middle_name = models.CharField(max_length=50, blank=True)
    owner_last_name = models.CharField(max_length=50, blank=True)
    owner_complete_address = models.TextField(blank=True)
    owner_email_address = models.CharField(max_length=50, blank=True)
    owner_telephone_number = models.CharField(max_length=50, blank=True, null=True)
    owner_mobile_number = models.CharField(max_length=50, blank=True)
    mode_of_payment = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class BusinessDetails(models.Model):
    application_number = models.OneToOneField(
        BusinessPermitApplication,
        on_delete=models.CASCADE,
    )
    name = models.TextField(blank=True, null=True)
    trade_name = models.TextField(blank=True, null=True)
    complete_business_address = models.TextField(blank=True, null=True)
    president_first_name = models.TextField(blank=True, null=True)
    president_middle_name = models.TextField(blank=True, null=True)
    president_last_name = models.TextField(blank=True, null=True)
    telephone_number = models.CharField(max_length=50, blank=True)
    email_address = models.CharField(max_length=50, blank=True)
    property_index_number = models.CharField(max_length=50, blank=True)
    area = models.FloatField(blank=True, null=True)
    total_employees = models.IntegerField(blank=True, null=True)
    residing_employees = models.IntegerField(blank=True, null=True)
    address_no = models.CharField(max_length=50, blank=True)
    subdivision = models.TextField(blank=True)
    unit_no = models.CharField(max_length=50, blank=True)
    floor_no = models.CharField(max_length=50, blank=True)
    house_no = models.CharField(max_length=50, blank=True)
    block_no = models.CharField(max_length=50, blank=True)
    lot_no = models.CharField(max_length=50, blank=True)
    building_no = models.CharField(max_length=50, blank=True)
    building_name = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    barangay = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class LessorDetails(models.Model):
    application_number = models.OneToOneField(
        BusinessPermitApplication,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    complete_address = models.TextField(blank=True)
    telephone_number = models.TextField(blank=True)
    mobile_number = PhoneNumberField(null=False, blank=True, default="")
    email_address = models.CharField(max_length=50, blank=True)
    gross_monthly_rental = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class BusinessActivity(models.Model):
    application_number = models.ForeignKey(BusinessPermitApplication,
                                           related_name="businessactivity",
                                           on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True)
    line_of_business = models.CharField(max_length=50, blank=True)
    capitalization = models.CharField(max_length=50, blank=True)
    essential = models.CharField(max_length=50, blank=True)
    units = models.CharField(max_length=20, blank=True, null=True)
    non_essential = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    application_year = models.CharField(max_length=20, blank=True, null=True)
    is_draft = models.BooleanField(default=False)
    remarks_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class ApplicationRequirements(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, default="")
    application_id = models.ForeignKey(
        BusinessPermitApplication,
        on_delete=models.CASCADE,
        related_name="businessapplicationrequirements",
        blank=True,
        default="")
    application_year = models.DateTimeField(auto_now_add=True)
    remarks_draft = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-updated_at',)


class RequirementFiles(models.Model):
    def get_user_image_folder(instance, filename):
        size = 6
        chars = string.ascii_uppercase + string.digits
        fileid = ''.join(random.choice(chars) for _ in range(size))
        filename = fileid + filename
        return "user_requirements/%s/business/%s/%s/" % (
            instance.requirement_id.user.username, instance.requirement_id.id,
            filename)

    requirement_id = models.ForeignKey(ApplicationRequirements,
                                       related_name='requirements',
                                       on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, blank=True)
    requirements_label = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    file = models.FileField(storage=PrivateMediaStorage(),
                            upload_to=get_user_image_folder,
                            null=True)


class BuildingPermitApplication(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    is_draft = models.BooleanField(default=True, blank=True)
    application_status = models.IntegerField(default=0)
    is_approve = models.BooleanField(default=False)
    is_disapprove = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    date_renewed = models.DateTimeField(null=True, blank=True)
    is_enrolled = models.BooleanField(default=False)
    last_submitted = models.DateTimeField(null=True, blank=True)
    latest_approver = models.ForeignKey('api.Department', on_delete= models.SET_NULL, null=True, blank=True)
    inspection_date = models.DateTimeField(null=True, blank=True)
    series_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class BuildingBasicInformation(models.Model):
    application_number = models.OneToOneField(
        BuildingPermitApplication,
        on_delete=models.CASCADE,
    )
    reference_number = models.CharField(max_length=20, blank=True)
    owner_first_name = models.TextField(blank=True)
    owner_middle_name = models.CharField(max_length=50, blank=True)
    owner_last_name = models.CharField(max_length=50, blank=True)
    owner_complete_address = models.TextField(blank=True)
    owner_zip_code = models.CharField(max_length=50, blank=True)
    owner_telephone_number = models.CharField(max_length=50, blank=True)
    ownership_type = models.CharField(max_length=50, blank=True)
    tin = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
            return 'Id: %s, Building application: %s' % (self.id, self.application_number)



class BuildingDetails(models.Model):
    application_number = models.OneToOneField(
        BuildingPermitApplication,
        on_delete=models.CASCADE,
    )
    area_no = models.CharField(max_length=50, blank=True)
    form_of_ownership = models.CharField(max_length=50, blank=True)
    lot_no = models.CharField(max_length=20, blank=True)
    blk_no = models.CharField(max_length=20, blank=True)
    tct_no = models.CharField(max_length=20, blank=True)
    tax_dec_no = models.CharField(max_length=20, blank=True)
    street = models.CharField(max_length=50, blank=True)
    barangay = models.TextField(blank=True)
    city = models.CharField(max_length=20, blank=True)
    scope_of_work = models.CharField(max_length=50, blank=True)
    scope_of_work_others = models.CharField(max_length=50, blank=True)
    character_of_occupancy = models.TextField(blank=True)
    character_of_occupancy_others = models.TextField(blank=True)
    property_type = models.CharField(max_length=20, blank=True)
    address_no = models.CharField(max_length=20, blank=True)
    lot_no_count = models.CharField(max_length=20, blank=True)
    phase_no = models.CharField(max_length=20, blank=True)
    subdivision_name = models.TextField(blank=True)
    district = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return 'Id: %s, Building application: %s' % (self.id, self.application_number)


class BuildingOtherDetails(models.Model):
    application_number = models.OneToOneField(
        BuildingPermitApplication,
        on_delete=models.CASCADE,
    )
    occupancy_classified = models.CharField(max_length=50, blank=True)
    total_estimated_cost = models.FloatField(blank=True)
    units = models.IntegerField()
    floor_area = models.IntegerField()
    lot_area = models.IntegerField()
    date_of_construction = models.DateTimeField(null=True, blank=True)
    date_of_completion = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class BuildingApplicationRequirements(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, default="")
    application_id = models.ForeignKey(
        BuildingPermitApplication,
        on_delete=models.CASCADE,
        related_name="buildingapplicationrequirements",
        blank=True,
        default="")
    application_year = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-updated_at',)


class BuildingRequirementFiles(models.Model):
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_user_image_folder(instance, filename):
        size = 6
        chars = string.ascii_uppercase + string.digits
        fileid = ''.join(random.choice(chars) for _ in range(size))
        filename = fileid + filename
        return "user_requirements/%s/building/%s/%s/" % (
            instance.requirement_id.user.username, instance.requirement_id.id,
            filename)

    requirement_id = models.ForeignKey(BuildingApplicationRequirements,
                                       related_name='buildingrequirements',
                                       on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, blank=True)
    requirements_label = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    file = models.FileField(storage=PrivateMediaStorage(),
                            upload_to=get_user_image_folder,
                            null=True)



class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey('core.User',
                               on_delete=models.CASCADE,
                               related_name='thread_sender')
                               
    receiver = models.ForeignKey('core.User',
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 related_name='thread_receiver')
    is_remarks = models.BooleanField(default=False, blank=True)
    business_id = models.ForeignKey(BusinessPermitApplication,
                                    related_name="businessremarks",
                                    blank=True,
                                    null=True,
                                    on_delete=models.CASCADE)
    building_id = models.ForeignKey(BuildingPermitApplication,
                                    related_name="buildingremarks",
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    subject = models.TextField(blank=False, null=False)
    status = models.CharField(max_length=50, blank=True, default="pending")
    department = models.CharField(max_length=100, blank=True, null=True)
    is_responded = models.BooleanField(default=False, blank=True)
    is_resolved = models.BooleanField(default=False, blank=True)
    is_delinquent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey('core.User',
                               on_delete=models.CASCADE,
                               related_name='messeage_sender')
    receiver = models.ForeignKey('core.User',
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 related_name='message_receiver')
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    body = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class MessageAttachment(models.Model):
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_user_image_folder(instance, filename):
        size = 6
        chars = string.ascii_uppercase + string.digits
        fileid = ''.join(random.choice(chars) for _ in range(size))
        filename = fileid + filename
        return "user_building_evaluation/%s" % (filename)

    message = models.ForeignKey(Message,
                                       on_delete=models.CASCADE, related_name="messageattachments")
    filename = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    file = models.FileField(storage=PrivateMediaStorage(),
                            upload_to=get_user_image_folder,
                            null=True)

class BuildingRequirementsChecklist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_number = models.ForeignKey(BuildingApplicationRequirements,
                                           related_name='buildingchecklist',
                                           on_delete=models.CASCADE)
    category = models.CharField(max_length=50, blank=True)
    value = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)




class AppointmentLimit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(blank=True, null=True)
    batch = models.CharField(max_length=50, blank=True)
    count = models.IntegerField(default=0, blank=True)
    remaining = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    batch = models.CharField(max_length=20, blank=True)
    appointment_date = models.DateTimeField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Soa(models.Model):
    date_issued = models.DateTimeField(null=True)
    year = models.CharField(max_length=20, blank=True)
    quarter = models.CharField(max_length=20, blank=True)
    paymode = models.CharField(max_length=20, blank=True)
    amount = models.FloatField(blank=True)
    business_application = models.ForeignKey(BusinessPermitApplication, on_delete=models.CASCADE, blank=True, null=True)
    building_application = models.ForeignKey(BuildingPermitApplication, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('core.User',
                               on_delete=models.CASCADE, null=True)
    appointment = models.OneToOneField(Appointment ,on_delete=models.SET_NULL, blank=True, null=True)
    application_type = models.CharField(max_length=50, blank=True)
    reference_number = models.CharField(max_length=50, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
            return self.reference_number

class Bill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_number = models.CharField(max_length=50, blank=True)
    soa = models.ForeignKey(Soa,
                        on_delete=models.CASCADE, null=True, related_name="bills")
    quarter = models.CharField(max_length=20, blank=True)
    amount = models.FloatField(blank=True)
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
            return self.reference_number

class BillFees(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill = models.ForeignKey(Bill,
                               on_delete=models.CASCADE, null=True, related_name="billfees")
    code = models.CharField(max_length=50, blank=True)
    fee_description = models.CharField(max_length=50, blank=True)
    amount = models.FloatField(blank=True)
    penalty = models.BooleanField(default=False)


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_type = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100, blank=True)
    index = models.IntegerField(default=0)
    business_index = models.IntegerField(default=0)
    building_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class BusinessDeptAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_application = models.ForeignKey(BusinessPermitApplication,
                               on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department,
                               on_delete=models.CASCADE, null=True)
    is_approve = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "Application: %s, Department: %s, Is Approved: %s" % (self.business_application, self.department, self.is_approve)

class BuildingDeptAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    building_application = models.ForeignKey(BuildingPermitApplication,
                               on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department,
                               on_delete=models.CASCADE, null=True)
    is_approve = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return "Application: %s, Department: %s, Is Approved: %s" % (self.building_application, self.department, self.is_approve)
    

class BankTransaction(models.Model):
    def get_slip_image_folder(instance, filename):
        size = 6
        chars = string.ascii_uppercase + string.digits
        fileid = ''.join(random.choice(chars) for _ in range(size))
        filename = fileid + filename
        return "payment/slip/%s/%s" % (
            instance.soa, filename)

    def get_receipt_image_folder(instance, filename):
        size = 6
        chars = string.ascii_uppercase + string.digits
        fileid = ''.join(random.choice(chars) for _ in range(size))
        filename = fileid + filename
        return "payment/receipt/%s/%s" % (
            instance.soa, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    soa = models.OneToOneField(Soa, on_delete=models.CASCADE)
    user = models.ForeignKey('core.User',
                               on_delete=models.CASCADE, null=True)
    bank = models.TextField(max_length=250)
    payment_date = models.DateTimeField()
    amount = models.FloatField()
    reference_no = models.TextField(max_length=250)
    is_verified = models.BooleanField(default=False)              
    payment_receipt = models.FileField(storage=PrivateMediaStorage(),
                            upload_to=get_receipt_image_folder,
                            null=True)
    payment_slip = models.FileField(storage=PrivateMediaStorage(),
                            upload_to=get_slip_image_folder,
                            null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
class LandbankTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant_ref_no = models.ForeignKey(Soa, on_delete=models.CASCADE, to_field="reference_number", related_name="landbank_transaction")
    particulars = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    payor_name = models.TextField(blank=True, null=True)
    payor_email = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)
    epp_ref_no = models.IntegerField(blank=True, null=True)
    payment_option = models.TextField(blank=True, null=True)
    date_stamp = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class PisoPayTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.TextField(blank=True, null=True)
    status_message = models.TextField(blank=True, null=True)
    settlement_status = models.TextField(blank=True, null=True)
    reference_count = models.TextField(blank=True, null=True)
    reference_number = models.TextField(blank=True, null=True)
    transaction_status_all = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    trace_number = models.ForeignKey(Soa, on_delete=models.CASCADE, to_field="reference_number", related_name="pisopay_transaction")
    payment_channel_code = models.TextField(blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    customer_email = models.TextField(blank=True, null=True)
    customer_phone = models.TextField(blank=True, null=True)
    transaction_id = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(null=True)
    posted_date = models.DateTimeField(null=True)
    timestamp = models.TextField(blank=True, null=True)
    hd = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Faq(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.question


class BusinessPermitFile(models.Model):
    def get_user_business_permit_folder(instance, filename):
        size = 6
        chars = string.ascii_uppercase + string.digits
        fileid = ''.join(random.choice(chars) for _ in range(size))
        filename = fileid + filename
        return "user_business_permit/%s/%s/%s/" % (
            instance.application_id.user.username, instance.application_id.id,
            filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_id = models.ForeignKey(
        BusinessPermitApplication,
        on_delete=models.CASCADE,
        related_name="businesspermitfiles",
        blank=True,
        default="")
    filename = models.CharField(max_length=100, blank=True)
    application_year = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    file = models.FileField(storage=PrivateMediaStorage(),
                            upload_to=get_user_business_permit_folder,
                            null=True)

    class Meta:
            ordering = ['created_at']

class MobileBuild(models.Model):
    def get_mobile_build_folder(instance, filename):
        size = 6
        chars = string.ascii_uppercase + string.digits
        fileid = ''.join(random.choice(chars) for _ in range(size))
        filename = fileid + filename
        return "mobile_builds/%s/%s/" % (
            instance.version, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.CharField(max_length=100, blank=True)
    file = models.FileField(storage=PrivateMediaStorage(),
                            upload_to=get_mobile_build_folder,
                            null=True)
    is_active = models.BooleanField(default=False, blank=True)
    for_maintenance = models.BooleanField(default=False, blank=True)
    update_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
            return 'Version: %s' % (self.version)

    class Meta:
            ordering = ['created_at']

class MobileDownload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_email = models.CharField(max_length=100, blank=True)
    version = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
            ordering = ['created_at']