import os
from django.core.mail import send_mail
from django.http import Http404
from api import models, serializers
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
class AssessmentEmailService():

    def __init__(self, id, **kwargs):
        self.id = id
        self.department = kwargs.get('department')

    def get_building_object(self):
        try:
            data = models.BuildingPermitApplication.objects.get(pk=self.id)
            serializer = serializers.BuildingApplicationListSerializer(
                data, many=False)
            return serializer.data
        except models.BuildingPermitApplication.DoesNotExist:
            raise Http404

    def get_department_object(self):
        try:
            data = models.Department.objects.get(pk=self.department)
            serializer = serializers.DepartmentSerializer(
                data, many=False)
            return serializer.data
        except models.Department.DoesNotExist:
            raise Http404

    def get_business_object(self):
        try:
            data = models.BusinessPermitApplication.objects.get(pk=self.id)
            serializer = serializers.BusinessApplicationListSerializer(data, many=False)
            return serializer.data
        except models.Department.DoesNotExist:
            raise Http404

    def send_business_application_status_complete(self):
        data = self.get_business_object()
        business_name = data['businessdetails']['name'] if data['businessdetails']['name'] != "" else data['businessdetails']['trade_name']
        user = data['user']
        subject = 'Business Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n this is to inform you that your online application for %s has been checked and verified and is now subject for Assessment. You would receive periodic emails regarding the current status of your application. You can likewise check your application status here by logging in to boss.bacoor.gov.ph. \n \n Thank you! \n City Government of Bacoor	\n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'], business_name)
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_business_application_status_incomplete(self):
        data = self.get_business_object()
        business_name = data['businessdetails']['name'] if data['businessdetails']['name'] != "" else data['businessdetails']['trade_name']
        user = data['user']
        subject = 'Business Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n This is to inform you that your online application for %s has been tagged as Incomplete. Kindly login to your account at boss.bacoor.gov.ph to check on your incomplete documents. From there you can update your application.  \n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'], business_name)
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_business_application_status_assessment_approved(self):
        data = self.get_business_object()
        business_name = data['businessdetails']['name'] if data['businessdetails']['name'] != "" else data['businessdetails']['trade_name']
        user = data['user']
        department = self.get_department_object()
        subject = 'Business Application Status'
        message = 'Hello Mr/Ms %s %s,\n \n This is to inform you that your online application for %s has been Approved by %s department. For further process we will send you an email notification about the current status of your application and also you can check your application here at boss.bacoor.gov.ph and login your account. \n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.'  % (user['first_name'], user['last_name'], business_name, department['name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_business_application_status_assessment_disapproved(self):
        data = self.get_business_object()
        business_name = data['businessdetails']['name'] if data['businessdetails']['name'] != "" else data['businessdetails']['trade_name']
        user = data['user']
        department = self.get_department_object()
        subject = 'Business Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n This is to inform you that your online application for %s has been Disapproved by %s department. Kindly login to at boss.bacoor.gov.ph to check the application comments. \n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'], business_name, department['name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_business_application_status_for_payment(self):
        data = self.get_business_object()
        business_name = data['businessdetails']['name'] if data['businessdetails']['name'] != "" else data['businessdetails']['trade_name']
        user = data['user']
        subject = 'Business Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n This is to inform you that your online application for %s is now ready for Payment. To check your Statement of Account (SOA), kindly login your account and go to Profile > Business and click Bill button\n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.'% (user['first_name'], user['last_name'], business_name)
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_business_application_status_for_compliance(self):
        data = self.get_business_object()
        business_name = data['businessdetails']['name'] if data['businessdetails']['name'] != "" else data['businessdetails']['trade_name']
        user = data['user']
        subject = 'Business Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n This is to inform you that your online application for %s has been tagged as for Compliance. Kindly login to your account at boss.bacoor.gov.ph to check remarks and update your application there.\n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.'% (user['first_name'], user['last_name'], business_name)
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_building_application_status_complete(self):
        data = self.get_building_object()
        user = data['user']
        subject = 'Building Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n This is to inform you that your online building application has been checked and verified. Your application is now subject for Inspection. Kindly expect further email updates regarding the status of your application. You can likewise login to boss.bacoor.gov.ph to verify your updated application status.\n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_building_application_status_incomplete(self):
        data = self.get_building_object()
        user = data['user']
        subject = 'Building Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n This is to inform you that your online building application has been tagged as Incomplete.  Kindly login to boss.bacoor.gov.ph to to check on your incomplete documents. From there you can update your application. \n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_building_application_status_inspection_schedule(self):
        data = self.get_building_object()
        subject = 'Inspection Schedule'
        user = data['user']
        fullname = "%s %s" % (user['first_name'], user['last_name'])
        date = data['inspection_date']
        date = parse_datetime(date)
        date = date.strftime('%B %d %Y')
        context = { "name": fullname, "inspection_date": date }
        html_message = render_to_string('inspectionnotif.html', context)
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject,'',from_email, to_email, html_message=html_message)

    def send_building_application_status_evaluation(self):
        data = self.get_building_object()
        user = data['user']
        subject = 'Building Application Status'
        message = 'Hello Mr/Ms %s %s \n \n This is to inform you that your online building application is now ready for Evaluation. This will take 1 business day to evaluate your application. You can login to boss.bacoor.gov.ph to check the status of your application here.\n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_building_application_status_assessment(self):
        data = self.get_building_object()
        user = data['user']
        subject = 'Building Application Status'
        message = 'Hello Mr/Ms %s %s \n \n This is to inform you that your online building application is now ready for Assessment.You can login to boss.bacoor.gov.ph to check the status of your application here. \n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]
        send_mail(subject, message, from_email, to_email)

    def send_building_application_status_compliance(self):
        data = self.get_building_object()
        user = data['user']
        subject = 'Building Application Status'
        message = 'Hello Mr/Ms %s %s  \n \n This is to inform you that your online building application has been tagged as for Compliance. Kindly login to your account at boss.bacoor.gov.ph to check remarks and update your application there.\n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_building_application_status_payment(self):
        data = self.get_building_object()
        user = data['user']
        subject = 'Building Application Status'
        message = 'Hello Mr/Ms %s %s \n \n This is to inform you that your online building application is now ready for Payment. To check your Statement of Account (SOA), kindly login your account here at boss.bacoor.gov.ph and go to Profile > Building and click Bill button.\n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_building_application_status_assessment_approved(self):
        data = self.get_building_object()
        department = self.get_department_object()
        user = data['user']
        td_no = data['buildingdetails']['tax_dec_no']
        subject = 'Business Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n This is to inform you that your online application for tax declaration no. %s has been Approved by %s. For further process we will send you an email notification about the current status of your application and also you can check your application here at boss.bacoor.gov.ph and login your account. \n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'], td_no, department['name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

    def send_building_application_status_assessment_disapproved(self):
        data = self.get_building_object()
        department = self.get_department_object()
        user = data['user']
        td_no = data['buildingdetails']['tax_dec_no']
        subject = 'Business Application Status'
        message = 'Hello Mr/Ms %s %s, \n \n This is to inform you that your online application for tax declaration no. %s has been Disapproved by %s department. kindly login to at boss.bacoor.gov.ph to check the application comments. \n \n Thank you! \n City Government of Bacoor \n This is an auto-generated email. Please do not reply.' % (user['first_name'], user['last_name'], td_no, department['name'])
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject, message, from_email, to_email)

class SoaEmailService():
    def __init__(self, id, **kwargs):
        self.id = id
    def get_soa_obj(self):
        try:
            data = models.Soa.objects.get(pk=self.id)
            serializer = serializers.SoaListSerializer(
                data, many=False)
            return serializer.data
        except models.Soa.DoesNotExist:
            raise Http404

    def send_rpt_soa_success(self):
        subject = "Payment Successful"
        data = self.get_soa_obj()
        user = data['user']
        fullname = "%s %s" % (user['first_name'], user['last_name'])
        td_no = data['building_application']['buildingdetails']['tax_dec_no']
        reference_number = data['reference_number']
        total_amount = data['amount']
        transaction_id = '# %d' % (data['landbank_transaction'][0]['epp_ref_no'])
        context = { "name": fullname, "td_no": td_no, "reference_number": reference_number, 
        "total_amount": total_amount, "transaction_id": transaction_id}
        html_message = render_to_string('soarptsuccess.html', context)
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject,'',from_email, to_email, html_message=html_message)


    def send_business_soa_success(self):
        subject = "Payment Successful"
        data = self.get_soa_obj()
        user = data['user']
        fullname = "%s %s" % (user['first_name'], user['last_name'])
        business_name = data['business_application']['businessdetails']['name'] if data['business_application']['businessdetails']['name'] != "" else data['business_application']['businessdetails']['trade_name']
        account_number = data['business_application']['account_number']
        total_amount = data['amount']
        reference_number = data['reference_number']
        transaction_id = '# %d' % (data['landbank_transaction'][0]['epp_ref_no'])
        context = { "name": fullname, "business_name": business_name, "account_number": account_number, 
        "total_amount": total_amount, "reference_number": reference_number, "transaction_id": transaction_id }
        html_message = render_to_string('soabusinesssuccess.html', context)
        from_email = os.getenv('DEFAULT_FROM_EMAIL')
        to_email = [user['email']]

        send_mail(subject,'',from_email, to_email, html_message=html_message)
