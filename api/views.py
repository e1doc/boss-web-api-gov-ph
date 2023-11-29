from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from rest_framework import status
from django.shortcuts import redirect
from staff import views
from api.serializers import BarangaySerializer, BusinessPermitApplicationSerializer, BusinessBasicInformationSerializer, BusinessDetailsSerializer, LessorDetailsSerializer, BusinessActivitySerializer, BusinessProfileSerializer, BuildingPermitApplicationSerializer, BuildingBasicInformationSerializer, BuildingDetailsSerializer, BuildingOtherDetailsSerializer, BusinessApplicationListSerializer, BuildingApplicationListSerializer, RequirementFilesSerializer, ApplicationRequirementsSerializer, BusinessRequirementsListSerializer, BuildingApplicationRequirementsSerializer, BuildingRequirementFilesSerializer, BuildingRequirementsListSerializer, ThreadSerializer, MessageSerializer, InquiryListSerializer, ThreadDetailsSerializer, BuildingRequirementsChecklistSerializer, AppointmentListSerializer, AppointmentSerializer, AppointmentLimitSerializer, SoaListSerializer, SoaSerializer, BillFeesSerializer, BillSerializer, MessageAttachmentsSerializer, DepartmentSerializer, BankTransactionSerializer, BankTransactionListSerializer, LandbankTransactionListSerializer, FaqSerializer, LandbankTransactionSerializer, BusinessPermitFilesSerializer, MobileBuildSerializer, MobileDownloadSerializer, PisoPayTransactionSerializer, PisoPayTransactionListSerializer

from api.models import BusinessPermitApplication, BusinessBasicInformation, BusinessDetails, LessorDetails, BusinessActivity, BuildingPermitApplication, BuildingBasicInformation, BuildingDetails, BuildingOtherDetails, RequirementFiles, ApplicationRequirements, BuildingRequirementFiles, BuildingApplicationRequirements, Thread, BuildingRequirementsChecklist, Appointment, AppointmentLimit, Soa, BusinessDeptAssessment, BuildingDeptAssessment, Department, MessageAttachment, BankTransaction, LandbankTransaction, Faq, BusinessPermitFile, MobileBuild, MobileDownload

from pprint import pprint
from django.core.exceptions import ObjectDoesNotExist
from api.custom_storage import PrivateMediaStorage
import traceback
import os
from rest_framework.permissions import AllowAny
from dateutil.parser import parse
from django.utils import timezone
from django.db.models import Q
from services.series import SeriesService
import requests
import json

class SendMail(APIView):
    def post(self, request, format=None):
        send_mail('Subject here',
                  'Here is the message.',
                  'regiojosh1@gmail.com', ['regiojosh1@gmail.com'],
                  fail_silently=False)
        return Response({"message": "Email Sent!"},
                        status=status.HTTP_201_CREATED)


class Redirect(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        baseUrl = os.getenv('BOSS_WEB_UI')
        if kwargs.get('uid', None) and kwargs.get('token', None):
            uid = kwargs.get('uid', None)
            token = kwargs.get('token', None)
            url = baseUrl + '/reset-password/' + uid + '/' + token
            response = redirect(url)
            return response


class BarangayList(APIView):
    def post(self, request, format=None):
        serializer = BarangaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response([serializer.data, serializer.errors],
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessPermitApplicationView(APIView):
    def get_business_object(self, pk):
        try:
            return BusinessPermitApplication.objects.get(pk=pk)
        except BusinessPermitApplication.DoesNotExist:
            raise Http404

    def get_business_details_object(self, application):
        try:
            business_details = application.businessdetails
            business_details_serializer = BusinessDetailsSerializer(
                business_details)
            return business_details_serializer.data
        except ObjectDoesNotExist:
            return {}

    def post(self, request, format=None):
        request.data['user'] = request.user.id
        application_serializer = BusinessPermitApplicationSerializer(
            data=request.data)

        if application_serializer.is_valid():
            application_serializer.save()
            return Response(application_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(application_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        request.data['user'] = request.user.id
        business_application = self.get_business_object(request.data['id'])
        if request.data['is_disapprove']:
            request.data['is_disapprove'] = False
        application_serializer = BusinessPermitApplicationSerializer(
            business_application, request.data)
        if application_serializer.is_valid():
            application_serializer.save()
            return Response(application_serializer.data)
        return Response(application_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        applications = BusinessPermitApplication.objects.filter(
            user=request.user.id, is_enrolled=False,
            is_approve=False).order_by('-updated_at')
        business_serializer = BusinessApplicationListSerializer(applications,
                                                                many=True)
        return Response(business_serializer.data)


class BusinessProfileListView(APIView):
    def get(self, request, format=None):
        enrolled_applications = BusinessPermitApplication.objects.filter(
            user=request.user.id, is_enrolled=True, on_renewal=False)
        approved_applications = BusinessPermitApplication.objects.filter(
            user=request.user.id,
            is_enrolled=False,
            is_approve=True,
            is_disapprove=False,
            is_draft=False,
            is_renewal=False)
        result_list = list(enrolled_applications) + list(approved_applications)
        print(list(approved_applications))
        business_serializer = BusinessApplicationListSerializer(result_list,
                                                                many=True)
        return Response(business_serializer.data)


class BasicInformationView(APIView):
    def get_basic_info_object(self, pk):
        try:
            return BusinessBasicInformation.objects.get(pk=pk)
        except BusinessBasicInformation.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        request.data[
            'reference_number'] = f"{request.data['application_number']}".zfill(
                7)
        basic_information_serializer = BusinessBasicInformationSerializer(
            data=request.data)
        if basic_information_serializer.is_valid():
            basic_information_serializer.save()
            return Response(basic_information_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(basic_information_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        basic_information = self.get_basic_info_object(request.data["id"])
        basic_info_serializer = BusinessBasicInformationSerializer(
            basic_information, request.data)
        if basic_info_serializer.is_valid():
            basic_info_serializer.save()
            return Response(basic_info_serializer.data)
        return Response(basic_info_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class BusinessDetailsView(APIView):
    def get_business_details_object(self, pk):
        try:
            return BusinessDetails.objects.get(pk=pk)
        except BusinessDetails.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        business_details_serializer = BusinessDetailsSerializer(
            data=request.data)
        if business_details_serializer.is_valid():
            business_details_serializer.save()
            return Response(business_details_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(business_details_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        business_details = self.get_business_details_object(request.data["id"])
        business_details_serializer = BusinessDetailsSerializer(
            business_details, request.data)
        if business_details_serializer.is_valid():
            business_details_serializer.save()
            return Response(business_details_serializer.data)
        return Response(business_details_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class LessorDetailsView(APIView):
    def get_lessor_details_object(self, pk):
        try:
            return LessorDetails.objects.get(pk=pk)
        except LessorDetails.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        lessor_details_serializer = LessorDetailsSerializer(data=request.data)
        if lessor_details_serializer.is_valid():
            lessor_details_serializer.save()
            return Response(lessor_details_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(lessor_details_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        lessor_details = self.get_lessor_details_object(request.data['id'])
        lessor_details_serializer = LessorDetailsSerializer(
            lessor_details, request.data)
        if lessor_details_serializer.is_valid():
            lessor_details_serializer.save()
            return Response(lessor_details_serializer.data)
        return Response(lessor_details_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class BusinessActivityViews(APIView):
    def get_activity_object(self, pk):
        try:
            return BusinessActivity.objects.get(pk=pk)
        except BusinessActivity.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        business_activities = []
        for activity in request.data:
            business_activity_serializer = BusinessActivitySerializer(
                data=activity)
            if business_activity_serializer.is_valid():
                business_activity_serializer.save()
                business_activities.append(business_activity_serializer.data)
            else:
                return Response(business_activity_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(business_activities, status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        business_activities = []
        for activity in request.data:
            business_activity = self.get_activity_object(activity["id"])
            business_activity_serializer = BusinessActivitySerializer(
                business_activity, activity)
            if business_activity_serializer.is_valid():
                business_activity_serializer.save()
                business_activities.append(business_activity_serializer.data)
            else:
                return Response(business_activity_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(business_activities, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        business_activities = BusinessActivity.objects.all().filter(
            Q(application_number=request.query_params['application_number']) & Q(is_active=True) & Q(is_draft=False) | Q(application_number=request.query_params['application_number']) & Q(is_active=False) & Q(remarks_draft=True))
        print(business_activities)
        activities_serializer = BusinessActivitySerializer(business_activities,
                                                           many=True)
        return Response(activities_serializer.data)


class BuildingPermitApplicationViews(APIView):
    def get_application(self, pk):
        try:
            return BuildingPermitApplication.objects.get(pk=pk)
        except BuildingPermitApplication.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        request.data['user'] = request.user.id
        building_permit_application_serializer = BuildingPermitApplicationSerializer(
            data=request.data)
        if building_permit_application_serializer.is_valid():
            building_permit_application_serializer.save()
            application = self.get_application(building_permit_application_serializer.data['id'])
            
            if application.is_enrolled != True:
                series = SeriesService(application=application)
                application.series_number = series.generate_series()

            application.save()
            return Response(building_permit_application_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(building_permit_application_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        building_applications = BuildingPermitApplication.objects.filter(
            user=request.user.id, is_enrolled=False).order_by('-updated_at')
        building_application_list_serializer = BuildingApplicationListSerializer(
            building_applications, many=True)
        return Response(building_application_list_serializer.data)

    def put(self, request, format=None):
        request.data['user'] = request.user.id
        building_application = self.get_application(request.data['id'])
        building_application_serializer = BuildingPermitApplicationSerializer(
            building_application, request.data)

        if building_application_serializer.is_valid():
            building_application_serializer.save()
            return Response(building_application_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(building_application_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class BuildingProfileViews(APIView):
    def get(self, request, format=None):
        # enrolled_applications = BuildingPermitApplication.objects.filter(
        #     user=request.user.id, is_enrolled=True)

        approved_applications = BuildingPermitApplication.objects.filter(
            user=request.user.id,
            is_approve=True,
            is_disapprove=False,
            is_draft=False)

        # result_list = list(enrolled_applications) + list(approved_applications)
        building_application_list_serializer = BuildingApplicationListSerializer(
            approved_applications, many=True)
        return Response(building_application_list_serializer.data)


class RealPropertyProfileViews(APIView):
    def get(self, request, format=None):
        enrolled_applications = BuildingPermitApplication.objects.filter(
            user=request.user.id, is_enrolled=True)
        building_application_list_serializer = BuildingApplicationListSerializer(
            enrolled_applications, many=True)
        return Response(building_application_list_serializer.data)


class BuildingBasicInformationViews(APIView):
    def get_basic_information_object(self, pk):
        try:
            return BuildingBasicInformation.objects.get(pk=pk)
        except BuildingBasicInformation.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        request.data[
            'reference_number'] = f"{request.data['application_number']}".zfill(
                7)
        building_basic_information_serializer = BuildingBasicInformationSerializer(
            data=request.data)
        if building_basic_information_serializer.is_valid():
            building_basic_information_serializer.save()
            return Response(building_basic_information_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(building_basic_information_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        building_basic_information = self.get_basic_information_object(
            request.data["id"])
        building_basic_information_serializer = BuildingBasicInformationSerializer(
            building_basic_information, request.data)
        if building_basic_information_serializer.is_valid():
            building_basic_information_serializer.save()
            return Response(building_basic_information_serializer.data)
        return Response(building_basic_information_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class BuildingDetailsViews(APIView):
    def get_details_object(self, pk):
        try:
            return BuildingDetails.objects.get(pk=pk)
        except BuildingDetails.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        building_details_serializer = BuildingDetailsSerializer(
            data=request.data)
        if building_details_serializer.is_valid():
            building_details_serializer.save()
            return Response(building_details_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(building_details_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        building_details = self.get_details_object(request.data["id"])
        building_details_serializer = BuildingDetailsSerializer(
            building_details, request.data)
        if building_details_serializer.is_valid():
            building_details_serializer.save()
            return Response(building_details_serializer.data)
        return Response(building_details_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class BuildingOtherDetailsViews(APIView):
    def get_other_details_object(self, pk):
        try:
            return BuildingOtherDetails.objects.get(pk=pk)
        except BuildingDetails.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        building_other_details_serializer = BuildingOtherDetailsSerializer(
            data=request.data)
        if building_other_details_serializer.is_valid():
            building_other_details_serializer.save()
            return Response(building_other_details_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(building_other_details_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        building_other_details = self.get_other_details_object(
            request.data["id"])
        building_other_details_serializer = BuildingOtherDetailsSerializer(
            building_other_details, request.data)
        if building_other_details_serializer.is_valid():
            building_other_details_serializer.save()
            return Response(building_other_details_serializer.data)
        return Response(building_other_details_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ApplicationRequirementsView(APIView):
    def get_application_req_obj(self, pk):
        try:
            return ApplicationRequirements.objects.get(pk=pk)
        except ApplicationRequirements.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        request.data['user'] = request.user.id
        application_requirement_serializer = ApplicationRequirementsSerializer(
            data=request.data)
        if application_requirement_serializer.is_valid():
            application_requirement_serializer.save()
            return Response(application_requirement_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(application_requirement_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        application_req = self.get_application_req_obj(
            request.query_params['id'])
        application_req_serializer = BusinessRequirementsListSerializer(
            application_req)
        return Response(application_req_serializer.data)


class BuildingApplicationRequirementsView(APIView):
    def get_building_application_req_obj(self, pk):
        try:
            return BuildingApplicationRequirements.objects.get(pk=pk)
        except BuildingApplicationRequirements.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        request.data['user'] = request.user.id
        building_application_requirement_serializer = BuildingApplicationRequirementsSerializer(
            data=request.data)
        if building_application_requirement_serializer.is_valid():
            building_application_requirement_serializer.save()
            return Response(building_application_requirement_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(building_application_requirement_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        building_application_req = self.get_building_application_req_obj(
            request.query_params['id'])
        building_application_req_serializer = BuildingRequirementsListSerializer(
            building_application_req)
        return Response(building_application_req_serializer.data)


class MessageAttachmentUploadView(APIView):
    def get_file_obj(self, pk):
        try:
            return MessageAttachment.objects.get(pk=pk)
        except MessageAttachment.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        try:
            data = {
                'message': request.data['message'],
                'filename': request.data['filename']
            }
            serializer = MessageAttachmentsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                evaluation = self.get_file_obj(serializer.data['id'])
                update_serializer = MessageAttachmentsSerializer(evaluation, request.data)
                if update_serializer.is_valid():
                    update_serializer.save()
                    return Response({
                        'message': 'OK',
                        'fileUrl': 'success',
                    })
                else:
                    print(update_serializer.errors)
                    return Response(update_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                    print(serializer.errors)
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileUploadView(APIView):
    def get_file_obj(self, pk):
        try:
            return RequirementFiles.objects.get(pk=pk)
        except RequirementFiles.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        file_obj = request.FILES['file']
        data = {
            'requirement_id': request.data['requirement_id'],
            'requirements_label': request.data['requirements_label'],
            'filename': request.data['filename']
        }
        checkIfRequirementExist = RequirementFiles.objects.filter(
            requirements_label=request.data['requirements_label'],
            requirement_id=request.data['requirement_id']).update(
                is_active=False)
        requirement_serializer = RequirementFilesSerializer(data=data)
        if requirement_serializer.is_valid():
            requirement_serializer.save()
            requirement = self.get_file_obj(requirement_serializer.data['id'])
            request.data['is_active'] = True
            update_serializer = RequirementFilesSerializer(
                requirement, request.data)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response({
                    'message': 'OK',
                    'fileUrl': 'success',
                })
            else:
                print(requirement_serializer.errors)
                return Response(requirement_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            print(requirement_serializer.errors)
            return Response(requirement_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class BuildingFileUploadView(APIView):
    def get_building_file_obj(self, pk):
        try:
            return BuildingRequirementFiles.objects.get(pk=pk)
        except BuildingRequirementFiles.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        try:
            buidling_file_obj = request.FILES['file']
            data = {
                'requirement_id': request.data['requirement_id'],
                'requirements_label': request.data['requirements_label'],
                'filename': request.data['filename']
            }
            checkIfRequirementExist = BuildingRequirementFiles.objects.filter(
                requirements_label=request.data['requirements_label'],
                requirement_id=request.data['requirement_id']).update(
                    is_active=False)
            building_requirement_serializer = BuildingRequirementFilesSerializer(
                data=data)
            if building_requirement_serializer.is_valid():
                building_requirement_serializer.save()
                building_requirement = self.get_building_file_obj(
                    building_requirement_serializer.data['id'])
                request.data['is_active'] = True
                building_update_serializer = BuildingRequirementFilesSerializer(
                    building_requirement, request.data)
                if building_update_serializer.is_valid():
                    building_update_serializer.save()
                    return Response({
                        'message': 'OK',
                        'fileUrl': 'success',
                    })
                else:
                    return Response(building_update_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                print(building_requirement_serializer.errors)
                return Response(building_requirement_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserTypeView(APIView):
    def post(self, request, format=None):
        return Response({"is_admin": request.user.is_staff})


class ThreadView(APIView):
    def post(self, request, format=None):
        try:
            request.data['sender'] = request.user.id
            thread_serializer = ThreadSerializer(data=request.data)
            if thread_serializer.is_valid():
                thread_serializer.save()
                return Response(thread_serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(thread_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            threads = Thread.objects.filter(sender=request.user.id)
            threads_list = ThreadDetailsSerializer(threads, many=True)
            return Response(threads_list.data)
        except:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserInquiryList(ListAPIView):
    pagination_class = views.BasicPagination

    def list(self, request):
        try:
            filtered_queryset = self.filter_queryset(
                Thread.objects.filter(
                    sender=request.user.id).order_by('-updated_at'))
            page = self.paginate_queryset(filtered_queryset)
            if page is not None:
                thread_serializer = ThreadSerializer(page, many=True)
                return self.get_paginated_response(thread_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SoaListView(ListAPIView):
    pagination_class = views.BasicPagination
    queryset = Soa.objects.all()

    def list(self, request):
        try:
            filter_query = request.query_params['filter']
            if filter_query == 'business':
                queryset = self.filter_queryset(
                    Soa.objects.filter(
                        user=request.user.id,
                        application_type='business').order_by('-updated_at'))
            elif filter_query == 'building':
                queryset = self.filter_queryset(
                    Soa.objects.filter(
                        user=request.user.id,
                        application_type='building').order_by('-updated_at'))
            elif filter_query == 'real_property':
                queryset = self.filter_queryset(
                    Soa.objects.filter(
                        user=request.user.id,
                        application_type='real_property').order_by('-updated_at'))
            else:
                queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = SoaListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSoaView(APIView):
    def post(self, request, format=None):
        try:
            soa = request.data['soa']
            soa['user'] = request.user.id
            bills = request.data['soa']['bills']
            soa_serializer = SoaSerializer(data=soa)
            soa_details = None
            prefix = ""
            if soa['application_type'] == 'business':
                prefix = "BPL-"
            elif soa['application_type'] == 'building':
                prefix = "OBO-"
            else:
                prefix = "RPT-"
            if soa_serializer.is_valid():
                soa_serializer.save()
                soa = Soa.objects.get(id=soa_serializer.data['id'])
                soa.reference_number = prefix + f"{soa_serializer.data['id']}".zfill(
                    8)
                soa.save()
                soa_details = SoaListSerializer(soa)
                for bill in bills:
                    bill['soa'] = soa_serializer.data['id']
                    bill_serializer = BillSerializer(data=bill)
                    if bill_serializer.is_valid():
                        bill_serializer.save()
                        for fee in bill['fees']:
                            fee['bill'] = bill_serializer.data['id']
                            fees_serializer = BillFeesSerializer(data=fee)
                            if fees_serializer.is_valid():
                                fees_serializer.save()

            return Response(
                {
                    "message": "Data Successfully created!",
                    "data": soa_details.data
                },
                status=status.HTTP_201_CREATED)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRemarksList(ListAPIView):
    pagination_class = views.BasicPagination

    def list(self, request):
        try:
            filtered_queryset = self.filter_queryset(
                Thread.objects.filter(
                    receiver=request.user.id).order_by('-updated_at'))
            page = self.paginate_queryset(filtered_queryset)
            if page is not None:
                thread_serializer = ThreadSerializer(page, many=True)
                return self.get_paginated_response(thread_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessageView(APIView):
    def get_thread_obj(self, pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        try:
            print('tread')
            print(request.data['thread'])
            request.data['sender'] = request.user.id
            thread = self.get_thread_obj(request.data['thread'])
            message_serializer = MessageSerializer(data=request.data)
            if message_serializer.is_valid():
                if request.user.is_staff == False:
                    thread.is_responded = False
                    thread.status = 'pending'
                    thread.save()
                message_serializer.save()
                return Response(message_serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(message_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InquiryView(APIView):
    def get_thread_obj(self, pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            if request.query_params['id'] != 'undefined':
                thread = self.get_thread_obj(request.query_params['id'])
                inquiry_serializer = InquiryListSerializer(thread, many=False)
                return Response(inquiry_serializer.data)
            else:
                return Response({})
        except:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ThreadResolveView(APIView):
    def get_thread_obj(self, pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise Http404

    def put(self, request, format=None):
        try:
            thread = self.get_thread_obj(request.data['id'])
            thread.is_resolved = request.data['is_resolved']
            thread.status = 'resolved'
            thread.save()
            return Response({
                "code": "ok",
                "message": "Data updated successfully."
            })
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyEnfrollmentView(APIView):
    def get(self, request, format=None):
        try:
            is_existing = False
            if request.query_params['type'] == 'business':
                business = BusinessPermitApplication.objects.filter(
                    account_number=request.query_params['id'])
                if len(business) > 0:
                    is_existing = True
            else:
                real_property = BuildingDetails.objects.filter(
                    tax_dec_no=request.query_params['id'])
                if len(real_property) > 0:
                    is_existing = True

            return Response({"is_existing": is_existing})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuildingRequirementsChecklistViews(APIView):
    def get_checklist_obj(self, pk):
        try:
            return BuildingRequirementsChecklist.objects.get(pk=pk)
        except BuildingRequirementsChecklist.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        try:
            building_checklist_serializer = BuildingRequirementsChecklistSerializer(
                data=request.data)
            if building_checklist_serializer.is_valid():
                building_checklist_serializer.save()
                return Response(building_checklist_serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(building_checklist_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            building_checklist = self.get_checklist_obj(request.data['id'])
            building_checklist_serializer = BuildingRequirementsChecklistSerializer(
                building_checklist, request.data)
            if building_checklist_serializer.is_valid():
                building_checklist_serializer.save()
                return Response(building_checklist_serializer.data)
            else:
                return Response(building_checklist_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuildingPermitApplicationProfileView(APIView):
    def get_building_object(self, pk):
        try:
            return BuildingPermitApplication.objects.get(pk=pk)
        except BuildingPermitApplication.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            application = self.get_building_object(
                request.query_params['application_number'])
            building_serializer = BuildingApplicationListSerializer(
                application)
            print("here")
            return Response(building_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BusinessPermitApplicationProfileView(APIView):
    def get_business_object(self, pk):
        try:
            return BusinessPermitApplication.objects.get(pk=pk)
        except BusinessPermitApplication.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            application = self.get_business_object(
                request.query_params['application_number'])
            business_serializer = BusinessApplicationListSerializer(
                application)
            return Response(business_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuildingRemarksThread(ListAPIView):
    def list(self, request):
        try:
            # Thread.objects.get(building_id=request.query_params['id'])

            data = Thread.objects.filter(
                is_remarks=True,
                building_id=request.query_params['id']).order_by('-created_at')
            if len(data) > 0:
                thread_serializer = ThreadDetailsSerializer(data[0])
                return Response(thread_serializer.data)
            else:
                return Response({})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BusinessRemarksThread(ListAPIView):
    def list(self, request):
        try:
            data = Thread.objects.filter(
                is_remarks=True,
                business_id=request.query_params['id']).order_by('-created_at')
            if len(data) > 0:
                thread_serializer = ThreadDetailsSerializer(data[0])
                return Response(thread_serializer.data)
            else:
                return Response({})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentView(APIView):
    def post(self, request):
        try:
            request.data['user'] = request.user.id
            has_appointment = len(
                Appointment.objects.filter(user=request.user.id,
                                           soa__pk=request.data['soa']))
            appointment_slot = AppointmentLimit.objects.filter(
                date=request.data['appointment_date'],
                batch=request.data['batch'])
            if len(appointment_slot) > 0:
                if has_appointment < 1:
                    if appointment_slot[0].remaining > 0:
                        appointment_serializer = AppointmentSerializer(
                            data=request.data)
                        if appointment_serializer.is_valid():
                            appointment_serializer.save()
                            soa_obj = Soa.objects.get(id=request.data['soa'])
                            update_obj = {
                                "appointment":
                                appointment_serializer.data["id"]
                            }
                            soa_serializer = SoaSerializer(soa_obj, update_obj)
                            if soa_serializer.is_valid():
                                soa_serializer.save()
                            appointment_slot[0].remaining = appointment_slot[
                                0].remaining - 1
                            appointment_slot[0].save()
                            return Response(appointment_serializer.data,
                                            status=status.HTTP_201_CREATED)
                        else:
                            return Response(appointment_serializer.errors,
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(
                            'There is no available slot for this date.',
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                        'You already have appointment for this day.',
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('There is no available slot for this date.',
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            request.data['user'] = request.user.id
            data = Appointment.objects.filter(user=request.user.id)

            appointment_serializer = AppointmentListSerializer(data, many=True)
            return Response(appointment_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            request.data['user'] = request.user.id
            print(request.data['old_appointment_date'])
            get_appointment = Appointment.objects.get(id=request.data['id'])
            has_appointment = len(
                Appointment.objects.filter(
                    user=request.user.id,
                    appointment_date=request.data['appointment_date'],
                    batch=request.data['batch'],
                    title=request.data['title']))
            appointment_slot = AppointmentLimit.objects.filter(
                date=request.data['appointment_date'],
                batch=request.data['batch'])
            old_appointment_slot = AppointmentLimit.objects.get(
                date=request.data['old_appointment_date'],
                batch=request.data['old_batch'])
            print(old_appointment_slot)
            if len(appointment_slot) > 0:
                if has_appointment < 1:
                    if appointment_slot[0].remaining > 0:
                        old_appointment_slot.remaining = old_appointment_slot.remaining + 1
                        old_appointment_slot.save()
                        appointment_serializer = AppointmentSerializer(
                            data=request.data)
                        soa_obj = Soa.objects.get(id=request.data['soa'])
                        if appointment_serializer.is_valid():
                            appointment_serializer.save()
                            soa_obj = Soa.objects.get(id=request.data['soa'])
                            update_obj = {
                                "appointment":
                                appointment_serializer.data["id"]
                            }
                            get_appointment.is_cancelled = True
                            get_appointment.save()
                            soa_serializer = SoaSerializer(soa_obj, update_obj)
                            if soa_serializer.is_valid():
                                soa_serializer.save()
                            appointment_slot[0].remaining = appointment_slot[
                                0].remaining - 1
                            appointment_slot[0].save()
                            return Response(appointment_serializer.data,
                                            status=status.HTTP_201_CREATED)
                        else:
                            return Response(appointment_serializer.errors,
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(
                            'There is no available slot for this date.',
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                        'You already have appointment for this day.',
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('There is no available slot for this date.',
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentLimitView(APIView):
    def get(self, request):
        try:
            month = int(request.query_params['month']) + 1
            data = AppointmentLimit.objects.filter(date__month=month)
            serializer = AppointmentLimitSerializer(data, many=True)
            print(request.query_params['month'])
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserBusinessAssessmentResult(APIView):
    def get(self, request):
        try:
            assessment_result = []
            business_application = request.query_params['business_application']
            departments = Department.objects.filter(
                Q(application_type="business")
                | Q(application_type="both")).order_by("business_index")
            print(departments)
            for department in departments:
                assessment = BusinessDeptAssessment.objects.filter(
                    business_application=business_application,
                    department=department.id,
                    is_active=True)
                if len(assessment) > 0:
                    assessment_status = assessment[
                        0].is_approve and "Approved" or "Disapproved"
                    set_data = {
                        "department": department.name,
                        "status": assessment_status,
                        "created_at": assessment[0].created_at
                    }
                    assessment_result.append(set_data)
                else:
                    set_data = {
                        "department": department.name,
                        "status": "Pending"
                    }
                    assessment_result.append(set_data)
            return Response(assessment_result)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserBuildingAssessmentResult(APIView):
    def get(self, request):
        try:
            assessment_result = []
            building_application = request.query_params['building_application']
            departments = Department.objects.filter(
                Q(application_type="building")
                | Q(application_type="both")).order_by("building_index")
            for department in departments:
                assessment = BuildingDeptAssessment.objects.filter(
                    building_application=building_application,
                    department=department.id,
                    is_active=True)
                if len(assessment) > 0:
                    status = assessment[
                        0].is_approve and "Approved" or "Disapproved"
                    set_data = {
                        "department": department.name,
                        "status": status,
                        "created_at": assessment[0].created_at
                    }
                    assessment_result.append(set_data)
                else:
                    set_data = {
                        "department": department.name,
                        "status": "Pending"
                    }
                    assessment_result.append(set_data)
            return Response(assessment_result)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserAppointmentList(ListAPIView):
    pagination_class = views.BasicPagination
    queryset = Appointment.objects.all()

    def list(self, request):
        queryset = self.filter_queryset(
            Appointment.objects.filter(
                user=request.user.id).order_by('-updated_at'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AppointmentListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class UserBusinessApplicationList(ListAPIView):
    pagination_class = views.BasicPagination
    queryset = BusinessPermitApplication.objects.all()

    def list(self, request):
        queryset = self.filter_queryset(
            BusinessPermitApplication.objects.filter(
                Q(user=request.user.id)).filter(Q(is_enrolled=False) | Q(is_renewed=True) | Q(is_approve=True) & Q(on_renewal=True)).order_by('-updated_at'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BusinessApplicationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class UserBuildingApplicationList(ListAPIView):
    pagination_class = views.BasicPagination
    queryset = BuildingPermitApplication.objects.all()

    def list(self, request):
        queryset = self.filter_queryset(
            BuildingPermitApplication.objects.filter(
                user=request.user.id,
                is_enrolled=False).order_by('-updated_at'))
        page = self.paginate_queryset(queryset)
        print(page)
        if page is not None:
            serializer = BuildingApplicationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

class DepartmentListView(APIView):
    def get(self, request):
        try:
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusinessActivityRenewalView(APIView):
    def get(self, request):
        try:
            application_number = request.query_params['application_number']
            activities = []
            active_activities = BusinessActivity.objects.filter(application_number=application_number, is_active=True)
            inactive_activities = BusinessActivity.objects.filter(application_number=application_number, is_active=False, is_draft = True)

            if len(inactive_activities) > 0:
                activities = inactive_activities
            else:
                activities = active_activities
            serializer = BusinessActivitySerializer(activities, many= True)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusinessRequirementsRenewal(APIView):
    def get(self, request):
        try:
            id = request.query_params['application_number']
            application_requirements = ApplicationRequirements.objects.filter(application_id=id, is_active=False, is_draft=True)
            serializer = ApplicationRequirementsSerializer(application_requirements, many=True)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusinessActiveRequirements(APIView):
    def get(self, request):
        try:
            id = request.query_params['application_number']
            application_requirements = ApplicationRequirements.objects.filter( Q(application_id=id) & Q(is_active=True) & Q(is_draft=False) | Q(application_id=id) & Q(is_active=False) & Q(is_draft=True) & Q(remarks_draft=True))
            serializer = ApplicationRequirementsSerializer(application_requirements, many=True)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RenewBusinessApplicationView(APIView):
    def post(self, request):
        try:
            id = request.data['application_number']

            update_active_activities = BusinessActivity.objects.filter(application_number=id, is_active=True, is_draft=False).update(is_active=False)
            update_active_requirements = ApplicationRequirements.objects.filter(application_id=id, is_active=True, is_draft=False).update(is_active=False)
            update_inactive_activities = BusinessActivity.objects.filter(application_number=id, is_active=False, is_draft=True).update(is_active=True, is_draft= False, remarks_draft=False)
            update_inactive_requirements = ApplicationRequirements.objects.filter(application_id=id, is_active=False, is_draft=True).update(is_active=True, is_draft=False, remarks_draft=False)
            return Response({'detail': 'Renewal Success!'})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LandBankSuccessRedirect(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        baseUrl = os.getenv('BOSS_WEB_UI')
        data = request.data
        url = baseUrl + "/payment/payment-success"
        payload = {
             "merchant_ref_no": data['MerchantRefNo'],
             "particulars": data["Particulars"],
             "amount": data["Amount"],
             "payor_name": data["PayorName"],
             "payor_email": data["PayorEmail"],
             "status": data["Status"],
             "epp_ref_no": data["EppRefNo"],
             "payment_option": data["PaymentOption"],
             "date_stamp": data["Datestamp"]
            }
        serializer = LandbankTransactionSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
        response = redirect(url)
        return response

class PisoPaySuccessCallback(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            baseUrl = os.getenv('BOSS_WEB_UI')
            data = request.data.data
            url = baseUrl + "/payment/payment-success"
            payload = {
                "status": data["status"],
                "status_message": data["statusMessage"],
                "settlement_status": data["settlementStatus"],
                "reference_count": data["referenceCount"],
                "reference_number": data["referenceNo"],
                "transaction_status_all": data["transactionStatusAll"],
                "amount": float(data["amount"]),
                "trace_number": data["traceNo"],
                "payment_channel_code": data["paymentChannelCode"],
                "customer_name": data["customerName"],
                "customer_email": data["customerEmail"],
                "customer_phone": data["customerPhone"],
                "transaction_id": data["transactionId"],
                "transaction_date": data["transactionDate"],
                "posted_date": data["postedDate"],
                "timestamp": data["timestamp"],
                "hd": data["hd"]
                }
            serializer = PisoPayTransactionSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
            return Response({"status": "Ok", "message": "Data successfully created!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class LandBankErrorRedirect(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        baseUrl = os.getenv('BOSS_WEB_UI')
        url = baseUrl + "/payment/payment-error"
        response = redirect(url)
        return response


class BankTransactionView(APIView):
    def get_file_obj(self, pk):
        try:
            return BankTransaction.objects.get(pk=pk)
        except BankTransaction.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        file_obj = request.FILES['payment_slip']
        data = {
            'soa': request.data['soa'],
            'bank': request.data['bank'],
            'payment_date': request.data['payment_date'],
            'amount': request.data['amount'],
            'reference_no': request.data['reference_no'],
            'filename': request.data['filename'],
            'user': request.user.id
        }
        serializer = BankTransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            slip = self.get_file_obj(serializer.data['id'])
            update_serializer = BankTransactionSerializer(
                slip, request.data)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response({
                    'message': 'OK',
                    'fileUrl': 'success',
                })
            else:
                print(requirement_serializer.errors)
                return Response(requirement_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            print(requirement_serializer.errors)
            return Response(requirement_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserBankTransactionListView(ListAPIView):
    pagination_class = views.BasicPagination
    def list(self, request):
        params = request.query_params
        transaction_type = params["type"]
        queryset = self.filter_queryset(
            BankTransaction.objects.filter(soa__application_type=transaction_type,
                user=request.user.id).order_by('-created_at'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BankTransactionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class UserLandbankTransactionListView(ListAPIView):
    pagination_class = views.BasicPagination
    def list(self, request):
        fil = request.query_params['filter']
        queryset = self.filter_queryset(
            LandbankTransaction.objects.filter(merchant_ref_no__user=request.user.id, merchant_ref_no__application_type=fil).order_by('-created_at')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LandbankTransactionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

class UserPisoPayTransactionListView(ListAPIView):
    pagination_class = views.BasicPagination
    def list(self, request):
        fil = request.query_params['filter']
        queryset = self.filter_queryset(
            PisoPayTransaction.objects.filter(trace_number__user=request.user.id, trace_number__application_type=fil).order_by('-created_at')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PisoPayTransactionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

class FaqView(APIView):
    def get(self, request, format=None):
        try:
            data = Faq.objects.all()
            serializer = FaqSerializer(data, many=True)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadBusinessView(APIView):
    def get_business_object(self, pk):
        try:
            return BusinessPermitApplication.objects.get(pk=pk)
        except BusinessPermitApplication.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            data = self.get_business_object(request.query_params['id'])
            serializer = BusinessApplicationListSerializer(data, many=False)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadBuildingView(APIView):
    def get_building_object(self, pk):
        try:
            return BuildingPermitApplication.objects.get(pk=pk)
        except BuildingPermitApplication.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            data = self.get_building_object(request.query_params['id'])
            serializer = BuildingApplicationListSerializer(data, many=False)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadInvoiceView(APIView):
    def get_soa_object(self, pk):
        try:
            return Soa.objects.get(pk=pk)
        except Soa.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            data = self.get_soa_object(request.query_params['id'])
            serializer = SoaListSerializer(data, many=False)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadAppointmentView(APIView):
    def get_appointment_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    
    def get(self, request, format=None):
        try:
            data = self.get_appointment_object(request.query_params['id'])
            serializer = AppointmentListSerializer(data, many=False)
            return Response(serializer.data)

        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActiveMobileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            data = MobileBuild.objects.filter(
                is_active=True
            )
            
            serializer = MobileBuildSerializer(data[0], many=False)

            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MobileBuildStatus(APIView):
    permission_classes = [AllowAny]

    def get_mobile_build_object(self, version):
        try:
            return MobileBuild.objects.get(version=version)
        except MobileBuild.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        try:

            data = self.get_mobile_build_object(request.data['version'])
            serializer = MobileBuildSerializer(data, many=False)
            return Response(serializer.data)

        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class MobileDownloadsCountView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):

        try:
            data = request.data
            hasDownloaded = MobileDownload.objects.filter(user_email=data["user_email"], version=data["version"])
            if len(hasDownloaded) < 1:
                serializer = MobileDownloadSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
        
                else:
                    return Response(requirement_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)

            serializer = MobileDownloadSerializer(hasDownloaded[0], many=False)
            return Response(serializer.data)

        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetPisoPaySessionView(APIView):
    def get(self, request, format=None):
        try:
            url = f"{os.getenv('PISOPAY_API_URL')}/session"
            pisopay_token = os.getenv('PISOPAY_API_TOKEN')
            headers = {'Authorization': f'Basic {pisopay_token}'}
            result = requests.get(url, headers=headers)
            response = json.loads(result.text)
            return Response(response, status=status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GeneratePisoPayTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        try:
            url = f"{os.getenv('PISOPAY_API_URL')}/token"
            pisopay_token = os.getenv('PISOPAY_API_TOKEN')
            headers = {'Authorization': f'Basic {pisopay_token}', 'Content-Type': 'application/json'}
            payload = json.dumps(request.data)
            result = requests.post(url, data=payload, headers=headers)
            response = json.loads(result.text)
            return Response(response, status=status.HTTP_200_OK)

        except Exception:
            traceback.print_exc()
            url = baseUrl + "/payment/payment-error"
            response = redirect(url)
            return response
