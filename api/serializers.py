from api.models import Barangay, BusinessPermitApplication, BusinessDetails, LessorDetails, BusinessActivity, BusinessBasicInformation, BuildingPermitApplication, BuildingBasicInformation, BuildingDetails, BuildingOtherDetails, ApplicationRequirements, RequirementFiles, BuildingApplicationRequirements, BuildingRequirementFiles, Thread, Message, BuildingRequirementsChecklist, Appointment, AppointmentLimit, Soa, Department, BusinessDeptAssessment, BuildingDeptAssessment, BillFees, Bill, MessageAttachment, BankTransaction, LandbankTransaction, Faq, BusinessPermitFile, MobileBuild, MobileDownload, PisoPayTransaction
from rest_framework import serializers
from core.models import User


class BarangaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Barangay
        fields = ['id', 'name']


class MessageAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class BusinessPermitApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPermitApplication
        fields = '__all__'
        read_only_fields = [
            'id', 'is_expired', 'date_renewed', 'created_at', 'updated_at'
        ]


class BusinessBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessBasicInformation
        fields = '__all__'


class BusinessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetails
        fields = '__all__'


class LessorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessorDetails
        fields = '__all__'


class BusinessActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessActivity
        fields = '__all__'


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        business_application = BusinessPermitApplicationSerializer(
            read_only=True)
        model = BusinessBasicInformation
        fields = '__all__'


class BuildingPermitApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPermitApplication
        fields = '__all__'
        read_only_fields = [
            'is_approve', 'is_expired', 'date_renewed', 'created_at',
            'updated_at '
        ]


class BuildingBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingBasicInformation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class BuildingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingDetails
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class BuildingOtherDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingOtherDetails
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ApplicationRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationRequirements
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'application_year']


class RequirementFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementFiles
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class BusinessPermitFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPermitFile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']



class BusinessRequirementsListSerializer(serializers.ModelSerializer):
    requirements = RequirementFilesSerializer(many=True, read_only=True)

    class Meta:
        model = ApplicationRequirements
        fields = [
            'id', 'created_at', 'updated_at', 'application_year',
            'requirements'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "middle_name", "is_staff", "department", "email", "phone_number"
        ]
        read_only_fields = ['created_at', 'updated_at']

class BusinessApplicationListSerializer(serializers.ModelSerializer):
    businessbasicinformation = BusinessBasicInformationSerializer(
        read_only=True)
    businessdetails = BusinessDetailsSerializer(read_only=True)
    lessordetails = LessorDetailsSerializer(read_only=True)
    businessapplicationrequirements = ApplicationRequirementsSerializer(
        many=True, read_only=True)
    user = UserSerializer(read_only=True)
    businessactivity = BusinessActivitySerializer(many=True, read_only=True)
    latest_approver = DepartmentSerializer(many=False, read_only=True)
    businesspermitfiles = BusinessPermitFilesSerializer(many=True, read_only=True)

    class Meta:
        model = BusinessPermitApplication
        fields = [
            'id',
            'user',
            'created_at',
            'updated_at',
            "last_submitted",
            "application_status",
            "is_draft",
            "is_approve",
            "is_enrolled",
            "is_disapprove",
            'account_number',
            'businessbasicinformation',
            "businessdetails",
            "lessordetails",
            "businessactivity",
            "businessapplicationrequirements",
            "latest_approver",
            "application_type",
            "is_renewed",
            "on_renewal",
            "last_renewal",
            "latest_approval_date",
            "businesspermitfiles",
            "is_renewal"
        ]


class BuildingApplicationRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingApplicationRequirements
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'application_year']


class BuildingRequirementFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingRequirementFiles
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        

class BuildingApplicationListSerializer(serializers.ModelSerializer):
    buildingbasicinformation = BuildingBasicInformationSerializer(
        read_only=True)
    buildingdetails = BuildingDetailsSerializer(read_only=True)
    buildingotherdetails = BuildingOtherDetailsSerializer(read_only=True)
    buildingapplicationrequirements = BuildingApplicationRequirementsSerializer(
        many=True, read_only=True)
    latest_approver = DepartmentSerializer(many=False, read_only=True)
    user = UserSerializer(many=False)

    class Meta:
        model = BuildingPermitApplication
        fields = [
            "id", "is_draft", "user", "application_status", "is_approve",
            "is_disapprove", "is_enrolled", "created_at",
            "last_submitted", "buildingbasicinformation", "buildingdetails",
            "buildingotherdetails", "buildingapplicationrequirements",
            "latest_approver", "reference_id", "inspection_date", "series_number"
        ]




class UserDetailsSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False)

    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "middle_name", "is_staff", "department"
        ]
        read_only_fields = ['created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ThreadMessageSerializer(serializers.ModelSerializer):
    sender = UserDetailsSerializer(many=False, read_only=True)
    messageattachments = MessageAttachmentsSerializer(many=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ThreadDetailsSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    receiver = UserSerializer(many=False, read_only=True)
    business_id = BusinessPermitApplicationSerializer(many=False, read_only=False)
    building_id = BuildingPermitApplicationSerializer(many=False, read_only=False)
    class Meta:
        model = Thread
        fields = [
            "id", "sender", "receiver", "subject", "is_remarks", "business_id",
            "building_id", "status", "department", "is_delinquent","created_at", "updated_at",
        ]
        read_only_fields = ['created_at', 'updated_at']


class ThreadSerializer(serializers.ModelSerializer):
    # sender =  UserSerializer(many=False,read_only=True)
    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class SoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soa
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class BillFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillFees
        fields = '__all__'


class InquiryListSerializer(serializers.ModelSerializer):

    messages = serializers.SerializerMethodField()
    sender = UserDetailsSerializer(many=False, read_only=True)
    receiver = UserSerializer(many=False, read_only=True)
    business_id = BusinessPermitApplicationSerializer(many=False)
    building_id = BuildingPermitApplicationSerializer(many=False)
    def get_messages(self, instance):
        messages = instance.messages.order_by("created_at")
        return ThreadMessageSerializer(messages, many=True).data

    class Meta:
        model = Thread
        fields = [
            'id', 'sender', 'receiver', 'is_responded', 'is_resolved',
            "is_remarks", "business_id", "building_id", 'subject', 'status',
            'messages', 'department','is_delinquent' ,'created_at'
        ]


class BuildingRequirementsChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingRequirementsChecklist
        fields = '__all__'


class BuildingRequirementsListSerializer(serializers.ModelSerializer):
    buildingrequirements = BuildingRequirementFilesSerializer(many=True,
                                                              read_only=True)
    buildingchecklist = BuildingRequirementsChecklistSerializer(many=True,
                                                                read_only=True)

    class Meta:
        model = BuildingApplicationRequirements
        fields = [
            'id', 'created_at', 'updated_at', 'application_year',
            'buildingrequirements', 'buildingchecklist'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class AdminAppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'title', 'batch', 'appointment_date', 'is_cancelled',
            'created_at', 'updated_at'
        ]


class AppointmentLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentLimit
        fields = '__all__'


class BillListSerializer(serializers.ModelSerializer):
    billfees = BillFeesSerializer(many=True)

    class Meta:
        model = Bill
        fields = "__all__"

class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = "__all__"
        
class LandbankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandbankTransaction
        fields = '__all__'

class PisoPayTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PisoPayTransaction
        fields = '__all__'

class SoaListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    building_application = BuildingApplicationListSerializer(many=False,
                                                             read_only=True)
    business_application = BusinessApplicationListSerializer(many=False,
                                                             read_only=True)
    appointment = AppointmentSerializer(many=False, read_only=True)
    banktransaction = BankTransactionSerializer(read_only=True)
    bills = BillListSerializer(many=True)
    landbank_transaction = LandbankTransactionSerializer(many=True, read_only=True)
    pisopay_transaction = PisoPayTransactionSerializer(many=True, read_only=True)
    class Meta:
        model = Soa
        fields = [
            "id", "date_issued", "amount", "business_application",
            "building_application", "banktransaction", "user", "appointment", "application_type",
            "reference_number", "year", "quarter", "paymode" ,"bills", "landbank_transaction", "pisopay_transaction", "is_verified","created_at",
            "updated_at",
        ]


class AppointmentListSerializer(serializers.ModelSerializer):
    soa = SoaListSerializer(many=False)

    class Meta:
        model = Appointment
        fields = '__all__'


class BusinessDeptAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDeptAssessment
        fields = '__all__'


class BusinessDeptAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDeptAssessment
        fields = '__all__'


class BuildingDeptAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingDeptAssessment
        fields = "__all__"


class BusinessDeptAssessmentListSerializer(serializers.ModelSerializer):
    business_application = BusinessApplicationListSerializer(many=False)
    department = DepartmentSerializer(many=False)

    class Meta:
        model = BusinessDeptAssessment
        fields = '__all__'


class BuildingDeptAssessmentListSerializer(serializers.ModelSerializer):
    building_application = BuildingApplicationListSerializer(many=False)
    department = DepartmentSerializer(many=False)

    class Meta:
        model = BuildingDeptAssessment
        fields = '__all__'

class BankTransactionListSerializer(serializers.ModelSerializer):
    soa = SoaListSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = BankTransaction
        fields = '__all__'


class LandbankTransactionListSerializer(serializers.ModelSerializer):
    merchant_ref_no = SoaListSerializer(many=False, read_only=True)
    class Meta:
        model = LandbankTransaction
        fields = '__all__'

class PisoPayTransactionListSerializer(serializers.ModelSerializer):
    trace_number = SoaListSerializer(many=False, read_only=True)
    class Meta:
        model = PisoPayTransaction
        fields = '__all__'

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'

class SoaAPIListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    building_application_id = serializers.ReadOnlyField(source='building_application.id')
    tax_dec_no = serializers.ReadOnlyField(source='building_application.buildingdetails.tax_dec_no')
    real_property_owner_first_name = serializers.ReadOnlyField(source='building_application.buildingbasicinformation.owner_first_name')
    real_property_owner_middle_name = serializers.ReadOnlyField(source='building_application.buildingbasicinformation.owner_middle_name')
    real_property_owner_last_name = serializers.ReadOnlyField(source='building_application.buildingbasicinformation.owner_last_name')
    banktransaction = BankTransactionSerializer(read_only=True)
    bills = BillListSerializer(many=True)
    landbank_transaction = LandbankTransactionSerializer(many=True, read_only=True)
    pisopay_transaction = PisoPayTransactionSerializer(many=True, read_only=True)
    business_account_number = serializers.ReadOnlyField(source='business_application.account_number')
    business_corporate_name = serializers.ReadOnlyField(source='business_application.businessdetails.name')
    business_trade_name = serializers.ReadOnlyField(source='business_application.businessdetails.trade_name')
    business_owner_first_name = serializers.ReadOnlyField(source='business_application.businessdetails.president_first_name')
    business_owner_middle_name = serializers.ReadOnlyField(source='business_application.businessdetails.president_middle_name')
    business_owner_last_name = serializers.ReadOnlyField(source='business_application.businessdetails.president_last_name')
    class Meta:
        model = Soa
        fields = [
            "id", "date_issued", "amount",
            "building_application_id", "tax_dec_no", "real_property_owner_first_name", "real_property_owner_middle_name", "real_property_owner_last_name", "business_account_number", "business_corporate_name", "business_trade_name","business_owner_first_name", "business_owner_middle_name", "business_owner_last_name", "banktransaction", "user", "appointment", "application_type",
            "reference_number", "year", "quarter", "paymode","bills", "landbank_transaction", "pisopay_transaction","is_verified","created_at",
            "updated_at"
        ]


class MobileBuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileBuild
        fields = '__all__'


class MobileDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileDownload
        fields = '__all__'
