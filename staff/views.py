from django.shortcuts import render
from api import serializers, models
from core.models import User
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse, Http404
from rest_framework.pagination import PageNumberPagination
import traceback
from datetime import date, timedelta
import datetime
from django.utils.dateparse import parse_datetime
from dateutil import tz, parser
from core.models import User
from django.db.models import Q
from itertools import chain
from functools import reduce
from queryset_sequence import QuerySetSequence
from rest_framework import viewsets
from django.db.models import Value
from django.db.models.functions import Concat
import json
from rest_framework.permissions import AllowAny
from services.email import AssessmentEmailService, SoaEmailService
from django.db.models.functions import TruncDay
from django.db.models import Count
import csv
# Create your views here.


class BasicPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class AppointmentLimitList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
    queryset = models.AppointmentLimit.objects.all()

    def list(self, request):
        queryset = self.filter_queryset(
            models.AppointmentLimit.objects.all().order_by('-updated_at'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            appointment_limit_serializer = serializers.AppointmentLimitSerializer(
                page, many=True)
            return self.get_paginated_response(
                appointment_limit_serializer.data)


class AppointmentLimitView(APIView):
    def post(self, request):
        try:
            dates = []
            is_existing = False
            for item in request.data['limit_set']:
                sdate = parse_datetime(item['start_date'])
                edate = parse_datetime(item['end_date'])
                delta = edate - sdate  # as timedelta
                for i in range(delta.days + 1):
                    day = sdate + timedelta(days=i)
                    date = models.AppointmentLimit.objects.filter(
                        date=day, batch=item['batch'])
                    if len(date) > 0:
                        is_existing = True
                    set_obj = {"date": day, "obj": item}
                    dates.append(set_obj)
            if is_existing:
                return Response(
                    {
                        'detail':
                        'There is an existing slot settings for the date you entered. Please try again.'
                    },
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                for date in dates:
                    set_obj = {
                        "date": date["date"],
                        "batch": date["obj"]["batch"],
                        "count": date["obj"]["count"],
                        "remaining": date["obj"]["count"]
                    }
                    serializer = serializers.AppointmentLimitSerializer(
                        data=set_obj)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print(serializer.errors)
            return Response({'detail': 'Success!'}, status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            month = int(request.query_params['month']) + 1
            data = models.AppointmentLimit.objects.filter(date__month=month)
            serializer = serializers.AppointmentLimitSerializer(data,
                                                                many=True)
            print(request.query_params['month'])
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminAppointmentList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
    queryset = models.Appointment.objects.all()

    def list(self, request):
        try:
            search = request.query_params['search']
            batch = request.query_params['batch']
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            # current_date = datetime.datetime.strptime(request.query_params['date'].split()[0], "%Y-%m-%dT%H:%M:%S")
            current_date = parse_datetime(request.query_params['date'])
            user = User.objects.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search))
            serializer = serializers.UserSerializer(user, many=True)
            querysets = []
            if search != "":
                if len(user) > 0:
                    for item in user:
                        _queryset = self.filter_queryset(
                            models.Appointment.objects.filter(
                                user=item.id)).order_by('-updated_at')
                        querysets.append(_queryset)
                    result_list = list(chain(querysets))
                    print(result_list)
                    combined_queryset = reduce(QuerySetSequence, result_list)
                    page = self.paginate_queryset(combined_queryset)
                    if page is not None:
                        appointment_serializer = serializers.AdminAppointmentSerializer(
                            page, many=True)
                        return self.get_paginated_response(
                            appointment_serializer.data)
                else:
                    return Response({
                        'links': {
                            "next": '',
                            "previous": ''
                        },
                        "count": 0,
                        "total_pages": 0,
                        "results": []
                    })
            else:
                queryset = self.filter_queryset(
                    models.Appointment.objects.filter(
                        batch=batch, appointment_date=current_date))
                page = self.paginate_queryset(queryset)
                if page is not None:
                    appointment_serializer = serializers.AdminAppointmentSerializer(
                        page, many=True)
                    return self.get_paginated_response(
                        appointment_serializer.data)

        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BusinessApplicationList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
    queryset = models.BusinessPermitApplication.objects.filter(
        Q(is_draft=False) & Q(is_enrolled=False) | Q(is_renewed=True) & Q(is_draft=False) & Q(on_renewal=True) | Q(application_status=4)).order_by('-updated_at')

    def list(self, request):
        # 0 = For Approval 1 = disapprove / incomplete, 2 = complete / assessment, 3 = for compliance, 4 = for payment
        filter_by = request.query_params['filter_by']
        search = request.query_params['id'].strip("0")

        if search != "":
            queryset = self.filter_queryset(
                models.BusinessPermitApplication.objects.filter(Q(id__icontains=search) | Q(account_number__contains=search) |  Q(businessdetails__name__icontains=search) | Q(businessdetails__trade_name__icontains=search)).filter(
                    Q(is_draft=False) & Q(is_enrolled=False) | Q(is_renewed=True) & Q(is_draft=False) & Q(on_renewal=True)))
        else:
            if filter_by == 'approved':
                queryset = self.filter_queryset(
                    models.BusinessPermitApplication.objects.filter(
                        Q(is_draft=False) &
                        Q(is_approve=True) &
                        Q(is_enrolled=False) &
                        Q(application_status=4) |
                        Q(is_renewed = True) & Q(is_draft=False) & Q(on_renewal=False) & Q(is_approve=True) & Q(application_status=4)).order_by('-updated_at'))
            elif filter_by == 'disapproved':
                queryset = self.filter_queryset(
                    models.BusinessPermitApplication.objects.filter(
                        Q(is_draft=False) &
                        Q(is_disapprove=True) &
                        Q(is_enrolled=False) &
                        Q(application_status=1) |
                        Q(is_renewed = True) & Q(is_draft=False) & Q(on_renewal=True) & Q(is_disapprove=True) & Q(application_status=1)).order_by('-updated_at'))
            elif filter_by == 'forEvaluation':
                queryset = self.filter_queryset(
                    models.BusinessPermitApplication.objects.filter(
                        Q(is_draft=False) &
                        Q(is_approve=False) &
                        Q(is_disapprove=False) &
                        Q(is_enrolled=False) &
                        Q(application_status=0) |
                        Q(is_renewed = True) & Q(is_draft=False) & Q(on_renewal=True) & Q(is_disapprove=False) & Q(application_status=0) ).order_by('-updated_at'))
            elif filter_by == 'forAssessment':
                queryset = self.filter_queryset(
                    models.BusinessPermitApplication.objects.filter(
                        Q(is_draft=False) &
                        Q(is_approve=False) &
                        Q(is_disapprove=False) &
                        Q(is_enrolled=False) &
                        Q(application_status=2) |
                        Q(is_renewed=True) & Q(is_draft=False) & Q(on_renewal=True) & Q(is_disapprove=False) & Q(application_status=2)).order_by('-updated_at'))
            elif filter_by == 'forCompliance':
                queryset = self.filter_queryset(
                    models.BusinessPermitApplication.objects.filter(
                        Q(is_draft=False) &
                        Q(is_approve=False) &
                        Q(is_disapprove=True) &
                        Q(is_enrolled=False) &
                        Q(application_status=3) |
                        Q(is_renewed=True) & Q(is_draft=False) & Q(on_renewal=True) & Q(is_disapprove=True) & Q(application_status=3)).order_by('-updated_at'))
            else:
                queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            business_serializer = serializers.BusinessApplicationListSerializer(
                page, many=True)
            return self.get_paginated_response(business_serializer.data)


class BuildingApplicationList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
    queryset = models.BuildingPermitApplication.objects.filter(
        is_draft=False, is_enrolled=False).order_by('-updated_at')

    def list(self, request):
        filter_by = request.query_params['filter_by']
        search = request.query_params['id'].strip("0")
        if search != "":
            queryset = self.filter_queryset(
                models.BuildingPermitApplication.objects.filter(
                    is_draft=False, id=search).order_by('-updated_at'))
        else:
            # 0 = For approval, 1 = disapprove / incomplete, 2 = complete, 3 = for inspection, 4 = for compliance, 5 = for payment / approve
            # 0 = for approval, 1 = incomplete, 2 = complete, 3 = for assessment, 4 complance, for payment
            if filter_by == 'approved':
                queryset = self.filter_queryset(
                    models.BuildingPermitApplication.objects.filter(
                        is_draft=False,
                        is_approve=True,
                        is_enrolled=False,
                        application_status=6).order_by('-updated_at'))
            elif filter_by == 'disapproved':
                queryset = self.filter_queryset(
                    models.BuildingPermitApplication.objects.filter(
                        is_draft=False,
                        is_disapprove=True,
                        is_enrolled=False,
                        application_status=1).order_by('-updated_at'))
            elif filter_by == 'isForInspection':
                queryset = self.filter_queryset(
                    models.BuildingPermitApplication.objects.filter(
                        is_draft=False,
                        is_disapprove=False,
                        is_enrolled=False,
                        is_approve=False,
                        application_status=3).order_by('-updated_at'))
            elif filter_by == 'isForCompliance':
                queryset = self.filter_queryset(
                    models.BuildingPermitApplication.objects.filter(
                        is_draft=False,
                        is_disapprove=False,
                        is_enrolled=False,
                        is_approve=False,
                        application_status=4 | Q(application_status = 5)).order_by('-updated_at'))
            elif filter_by == 'forApproval':
                queryset = self.filter_queryset(
                    models.BuildingPermitApplication.objects.filter(
                        is_draft=False,
                        is_approve=False,
                        is_disapprove=False,
                        is_enrolled=False,
                        application_status=0).order_by('-updated_at'))

            elif filter_by == 'isComplete':
                queryset = self.filter_queryset(
                    models.BuildingPermitApplication.objects.filter(
                        is_draft=False,
                        is_approve=False,
                        is_disapprove=False,
                        is_enrolled=False,
                        application_status=2).order_by('-updated_at'))
            else:
                queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            building_serializer = serializers.BuildingApplicationListSerializer(
                page, many=True)
            return self.get_paginated_response(building_serializer.data)


class ThreadList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def list(self, request):
        try:
            queryset = models.Thread.objects.annotate(search_name=Concat('sender__first_name', Value(' '), 'sender__last_name'))
            search = request.query_params['search']
            department = request.query_params['department']
            print(department)
            if department != 'all' and department != '':
                queryset = queryset.filter(department=department)
            
            if request.query_params['filter_by'] == 'all_inquiries':
                filtered_queryset = self.filter_queryset(
                    queryset.filter(is_remarks=False, is_delinquent=False).filter(search_name__icontains=search).order_by('-updated_at'))
            else:
                filtered_queryset = self.filter_queryset(
                    queryset.filter(
                        is_remarks=False,
                        is_delinquent=False,
                        is_responded=False).filter(search_name__icontains=search).order_by('-updated_at'))
            page = self.paginate_queryset(filtered_queryset)
            if page is not None:
                thread_serializer = serializers.ThreadDetailsSerializer(
                    page, many=True)
                return self.get_paginated_response(thread_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemarksThreadList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def list(self, request):
        try:
            queryset = models.Thread.objects.annotate(search_name=Concat('sender__first_name', Value(' '), 'sender__last_name'))
            search = request.query_params['search']
            if request.query_params['filter_by'] == 'all_inquiries':
                filtered_queryset = self.filter_queryset(
                    queryset.filter(
                        is_remarks=True, is_delinquent=False).filter(Q(search_name__icontains=search) | Q(building_id__buildingbasicinformation__reference_number__icontains=search) | Q(business_id__businessbasicinformation__reference_number__icontains=search)).order_by('-updated_at'))
            else:
                filtered_queryset = self.filter_queryset(
                    queryset.filter(
                        is_remarks=True,
                        is_delinquent=False,
                        is_responded=False).filter(Q(search_name__icontains=search)| Q(building_id__buildingbasicinformation__reference_number__icontains=search) | Q(business_id__businessbasicinformation__reference_number__icontains=search) ).order_by('-updated_at'))
            page = self.paginate_queryset(filtered_queryset)
            if page is not None:
                thread_serializer = serializers.ThreadDetailsSerializer(
                    page, many=True)
                return self.get_paginated_response(thread_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DelinquentThreadList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
    def list(self, request):
        try:
            queryset = models.Thread.objects.annotate(search_name=Concat('sender__first_name', Value(' '), 'sender__last_name'))
            search = request.query_params['search']
            if request.query_params['filter_by'] == 'all_inquiries':
                filtered_queryset = self.filter_queryset(
                    queryset.filter(
                        is_delinquent=True).filter(Q(search_name__icontains=search) | Q(building_id__buildingdetails__tax_dec_no__icontains=search)).order_by('-updated_at'))
            else:
                filtered_queryset = self.filter_queryset(
                    queryset.filter(
                        is_delinquent=True,
                        is_responded=False).filter(Q(search_name__icontains=search) | Q(building_id__buildingdetails__tax_dec_no__icontains=search)).order_by('-updated_at'))
            page = self.paginate_queryset(filtered_queryset)
            if page is not None:
                thread_serializer = serializers.ThreadDetailsSerializer(
                    page, many=True)
                return self.get_paginated_response(thread_serializer.data)

        except Exception:
                traceback.print_exc()
                return Response(
                    {'detail': 'Something went wrong. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ThreadRespondView(APIView):
    permission_classes = [IsAdminUser]

    def get_thread_obj(self, pk):
        try:
            return models.Thread.objects.get(pk=pk)
        except models.Thread.DoesNotExist:
            raise Http404

    def put(self, request, format=None):
        try:
            thread = self.get_thread_obj(request.data['id'])
            if thread.is_remarks != True:
                thread.is_responded = request.data['is_responded']
                thread.status = 'responded'
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


class BusinessPermitApplicationView(APIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def get_business_object(self, pk):
        try:
            return models.BusinessPermitApplication.objects.get(pk=pk)
        except models.BusinessPermitApplication.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            applications = models.BusinessPermitApplication.objects.filter(
                is_draft=False).order_by('-updated_at')
            business_serializer = serializers.BusinessApplicationListSerializer(
                applications, many=True)
            return Response(business_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # 0 = For Approval 1 = disapprove / incomplete, 2 = complete / assessment, 3 = for compliance, 4 = for payment
            application = self.get_business_object(request.data['id'])
            es = AssessmentEmailService(request.data['id'])
            if request.data['status'] == 1:
                es.send_business_application_status_incomplete()
                application.is_disapprove = True
                application.application_status = 1
                application.is_approve = False
                if application.on_renewal:
                    update_active_activities = models.BusinessActivity.objects.filter(application_number=request.data['id'], is_active=True, is_draft=False).update(is_active=False, is_draft=True, remarks_draft=True)
                    update_active_requirements = models.ApplicationRequirements.objects.filter(application_id=request.data['id'], is_active=True, is_draft=False).update(is_active=False, is_draft=True, remarks_draft=True)
            elif request.data['status'] == 2:
                es.send_business_application_status_complete()
                application.is_disapprove = False
                application.application_status = 2
            elif request.data['status'] == 3:
                application.is_disapprove = True
                application.is_approve = False
                application.application_status = 3
                es.send_business_application_status_for_compliance()
                if application.on_renewal:
                    update_active_activities = models.BusinessActivity.objects.filter(application_number=request.data['id'], is_active=True, is_draft=False).update(is_active=False,is_draft=True, remarks_draft=True)
                    update_active_requirements = models.ApplicationRequirements.objects.filter(application_id=request.data['id'], is_active=True, is_draft=False).update(is_active=False, is_draft=True, remarks_draft=True)
            elif request.data['status'] == 4:
                application.latest_approval_date = datetime.datetime.now().date()
                if application.on_renewal:
                    application.last_renewal = datetime.datetime.now().date()
                application.is_disapprove = False
                application.is_approve = True
                application.application_status = 4
                application.on_renewal = False
                es.send_business_application_status_for_payment()
            application.account_number = request.data['account_number']
            application.save()
            return Response({'detail': 'Data updated successfully!'})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuildingPermitApplicationView(APIView):
    permission_classes = [IsAdminUser]

    def get_building_object(self, pk):
        try:
            return models.BuildingPermitApplication.objects.get(pk=pk)
        except models.BuildingPermitApplication.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        try:
            applications = models.BuildingPermitApplication.objects.filter(
                is_draft=False)
            building_serializer = serializers.BuildingApplicationListSerializer(
                applications, many=True)
            return Response(building_serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # 0 = For Approval 1 = disapprove / incomplete, 2 = complete, 3 = for inspection, 4 = for compliance, 5 = for payment / approve

            # 0 = For Approval, 1 = Incomplete, 2 = For Inspection, 3 = For Assessment 4 = For Compliance, 5 For Compliance, 6 = For Payment
            application = self.get_building_object(request.data['id'])
            es = AssessmentEmailService(request.data['id'])
            if request.data['status'] == 1:
                es.send_building_application_status_incomplete()
                application.is_disapprove = True
                application.application_status = 1
            elif request.data['status'] == 2:
                es.send_building_application_status_complete()
                application.is_disapprove = False
                application.application_status = 2
                application.inspection_date = request.data['inspection_date']
            elif request.data['status'] == 3:
                es.send_building_application_status_assessment()
                application.is_disapprove = False
                application.application_status = 3
            elif request.data['status'] == 4:
                es.send_building_application_status_compliance()
                application.is_disapprove = True
                application.application_status = 4
            elif request.data['status'] == 5:
                es.send_building_application_status_compliance()
                application.is_disapprove = True
                application.application_status = 5
            elif request.data['status'] == 6:
                es.send_building_application_status_payment()
                application.is_disapprove = False
                application.is_approve = True
                application.application_status = 6
            application.save()
            if application.application_status == 2:
                es.send_building_application_status_inspection_schedule()
            return Response({'detail': 'Data updated successfully!'})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        try:
            users_count = User.objects.filter(is_staff=False).count()
            business_count = models.BusinessPermitApplication.objects.filter(
                is_draft=False, is_enrolled=False).count()
            building_count = models.BuildingPermitApplication.objects.filter(
                is_draft=False, is_enrolled=False).count()
            pending_inquiries = models.Thread.objects.filter(
                status='pending', is_remarks=False).count()
            all_inquiries = models.Thread.objects.filter(is_remarks=False).count()
            enrolled_business_count = models.BusinessPermitApplication.objects.filter(
                is_enrolled=True).count()
            enrolled_property_count = models.BuildingPermitApplication.objects.filter(
                is_enrolled=True).count()
            bank_transaction_count = models.BankTransaction.objects.all().count()
            return Response({
                'business': business_count,
                'building': building_count,
                'pending_inquiries': pending_inquiries,
                'all_inquiries': all_inquiries,
                'users_count': users_count,
                'enrolled_business_count': enrolled_business_count,
                'enrolled_property_count': enrolled_property_count,
                'bank_transaction_count': bank_transaction_count
            })
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyGroupView(APIView):
    def get(self, request, format=None):
        group = request.user.groups.values_list('name', flat=True)
        return Response(group)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all().order_by('index')
    serializer_class = serializers.DepartmentSerializer


class DepartmentList(APIView):
    def get(self, request, format=None):
        try:
            _filter = request.query_params["filter"]
            orderBy = _filter == 'business' and 'business_index' or 'building_index'
            print(_filter, orderBy)
            data = models.Department.objects.filter(
                Q(application_type=_filter)
                | Q(application_type='both')).order_by(orderBy)
            serializer = serializers.DepartmentSerializer(data, many=True)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BusinessDeptAssessmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            business_application = request.data['business_application']
            is_approve = request.data["is_approve"]
            user_serializer = serializers.UserSerializer(request.user,
                                                         many=False)
            department = user_serializer.data["department"]
            is_existing = models.BusinessDeptAssessment.objects.filter(
                business_application=business_application,
                department=department,
                is_active=True)
            department = user_serializer.data["department"]
            es = AssessmentEmailService(business_application, department = department)
            set_data = {
                    "business_application": business_application,
                    "department": department,
                    "is_approve": is_approve
            }
            if len(is_existing) < 1:
                serializer = serializers.BusinessDeptAssessmentSerializer(
                    data=set_data)
                if serializer.is_valid():
                    serializer.save()
                    if is_approve:
                        es.send_business_application_status_assessment_approved()
                    else:
                        es.send_business_application_status_assessment_disapproved()
                    update_application = models.BusinessPermitApplication.objects.get(
                        id=business_application)
                    update_application.latest_approver = request.user.department
                    update_application.save()
                    return Response(
                        {"detail": "Application was successfully assessed!"})
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                update_serializer = serializers.BusinessDeptAssessmentSerializer(is_existing[0], set_data)
                if update_serializer.is_valid():
                    update_serializer.save()
                    if is_approve:
                        es.send_business_application_status_assessment_approved()
                    else:
                        es.send_business_application_status_assessment_disapproved()
                return Response(
                        {"detail": "Application was successfully assessed!"})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            assessment_result = []
            business_application = request.query_params['business_application']
            departments = models.Department.objects.filter(
                Q(application_type="business")
                | Q(application_type="both")).order_by("business_index")
            for department in departments:
                assessment = models.BusinessDeptAssessment.objects.filter(
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


class BuildingDeptAssessmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            building_application = request.data['building_application']
            is_approve = request.data["is_approve"]
            user_serializer = serializers.UserSerializer(request.user,
                                                         many=False)
            department = user_serializer.data["department"]
            es = AssessmentEmailService(request.data['building_application'], department = department)
            is_existing = models.BuildingDeptAssessment.objects.filter(
                building_application=building_application,
                department=department,
                is_active=True)
            set_data = {
                    "building_application": building_application,
                    "department": department,
                    "is_approve": is_approve
            }
            if (len(is_existing) < 1):
                serializer = serializers.BuildingDeptAssessmentSerializer(
                    data=set_data)
                if serializer.is_valid():
                    serializer.save()
                    if(is_approve):
                        es.send_building_application_status_assessment_approved()
                    else:
                        es.send_building_application_status_assessment_disapproved()
                    update_application = models.BuildingPermitApplication.objects.get(
                        id=building_application)
                    update_application.latest_approver = request.user.department
                    update_application.save()
                    return Response(
                        {"detail": "Application was successfully assessed!"})
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                update_serializer = serializers.BuildingDeptAssessmentSerializer(is_existing[0], set_data)
                if update_serializer.is_valid():
                    update_serializer.save()
                    if(is_approve):
                        es.send_building_application_status_assessment_approved()
                    else:
                        es.send_building_application_status_assessment_disapproved()
                    return Response(
                        {"detail": "Application was successfully assessed!"})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            assessment_result = []
            building_application = request.query_params['building_application']
            departments = models.Department.objects.filter(
                Q(application_type="building")
                | Q(application_type="both")).order_by("building_index")
            for department in departments:
                assessment = models.BuildingDeptAssessment.objects.filter(
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


class CheckBusinessDeptIfCanAssess(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            user_serializer = serializers.UserSerializer(request.user,
                                                         many=False)
            user_department = models.Department.objects.get(
                id=user_serializer.data["department"])
            business_application = request.query_params['business_application']
            departments = models.Department.objects.filter(
                Q(application_type="business")
                | Q(application_type="both")).order_by(
                    'business_index').last()
            is_last_department = False
            if departments.name == user_department.name:
                is_last_department = True
            if user_department.business_index > 1:
                previous_index = user_department.business_index - 1
                previous_department = models.Department.objects.get(
                    Q(application_type="business")
                    | Q(application_type="both"),
                    business_index=previous_index)
                is_assess = models.BusinessDeptAssessment.objects.filter(
                    business_application=business_application,
                    department=previous_department.id,
                    is_active=True)
                if len(is_assess) > 0:
                    return Response({
                        'can_assess': True,
                        'last_department': is_last_department
                    })
                else:
                    return Response({
                        'can_assess': False,
                        'last_department': is_last_department
                    })
            else:
                return Response({
                    'can_assess': True,
                    'last_department': is_last_department
                })
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckBuildingDeptIfCanAssess(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            user_serializer = serializers.UserSerializer(request.user,
                                                         many=False)
            user_department = models.Department.objects.get(
                id=user_serializer.data["department"])
            building_application = request.query_params['building_application']
            departments = models.Department.objects.filter(
                Q(application_type="building")
                | Q(application_type="both")).order_by(
                    'building_index').last()
            is_last_department = False
            if departments.name == user_department.name:
                is_last_department = True
            if user_department.building_index > 1:
                previous_index = user_department.building_index - 1
                previous_department = models.Department.objects.get(
                    Q(application_type="building")
                    | Q(application_type="both"),
                    building_index=previous_index)
                is_assess = models.BuildingDeptAssessment.objects.filter(
                    building_application=building_application,
                    department=previous_department.id,
                    is_active=True)
                if len(is_assess) > 0:
                    return Response({
                        'can_assess': True,
                        'last_department': is_last_department
                    })
                else:
                    return Response({
                        'can_assess': False,
                        'last_department': is_last_department
                    })
            else:
                return Response({
                    'can_assess': True,
                    'last_department': is_last_department
                })
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForBusinessAssessmentList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
    def list(self, request):
        search = request.query_params['search']
        user_serializer = serializers.UserSerializer(request.user, many=False)
        user_department = models.Department.objects.get(
            id=user_serializer.data["department"])
        current_index = user_department.business_index
        # if not first department to assess
        if current_index > 1:
            applications = []
            previous_assessor = models.Department.objects.get(
                Q(application_type='business') | Q(application_type='both'),
                business_index=current_index - 1)

            business_assessment = models.BusinessDeptAssessment.objects.filter(Q(business_application__account_number__icontains=search) | Q(business_application__businessbasicinformation__reference_number__icontains=search) |
                Q(business_application__businessdetails__name__icontains=search) |  Q(business_application__businessdetails__trade_name__icontains=search),
                    department=previous_assessor, is_active=True)
            for assessment in business_assessment:
                application = models.BusinessPermitApplication.objects.get(
                    id=assessment.business_application.id)
                check_if_assessed = models.BusinessDeptAssessment.objects.filter(
                    department=user_department.id,
                    is_active=True,
                    business_application=assessment.business_application.id)
                if len(check_if_assessed) < 1:
                    applications.append(application)
            page = self.paginate_queryset(applications)
            if page is not None:
                serializer = serializers.BusinessApplicationListSerializer(
                    page, many=True)
                return self.get_paginated_response(serializer.data)
        # if first department to assess
        elif current_index == 1:
            querysets = []
            applications = models.BusinessPermitApplication.objects.filter(Q(account_number__icontains=search) | Q(businessbasicinformation__reference_number__icontains=search) |
                Q(businessdetails__name__icontains=search) |  Q(businessdetails__trade_name__icontains=search),
                application_status=2)
            for item in applications:
                is_assess = models.BusinessDeptAssessment.objects.filter(
                    business_application=item.id, is_active=True)
                if len(is_assess) < 1:
                    querysets.append(item)
            page = self.paginate_queryset(querysets)

            if page is not None:
                serializer = serializers.BusinessApplicationListSerializer(
                    page, many=True)
                return self.get_paginated_response(serializer.data)

        else:
            return Response({
                'links': {
                    "next": '',
                    "previous": ''
                },
                "count": 0,
                "total_pages": 0,
                "results": []
            })


class ForBuildingAssessmentList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def list(self, request):
        search = request.query_params['search']
        user_serializer = serializers.UserSerializer(request.user, many=False)
        user_department = models.Department.objects.get(
            id=user_serializer.data["department"])
        current_index = user_department.building_index
        # if not first department to assess
        if current_index > 1:
            applications = []
            previous_assessor = models.Department.objects.get(
                Q(application_type='building') | Q(application_type='both'),
                building_index=current_index - 1)
            building_assessment = models.BuildingDeptAssessment.objects.filter(Q(building_application__buildingbasicinformation__reference_number__icontains=search) | Q(building_application__buildingdetails__tax_dec_no__icontains=search) |  Q(building_application__buildingdetails__tax_dec_no__icontains=search) | Q(building_application__series_number__icontains=search),
                department=previous_assessor, is_active=True)
            for assessment in building_assessment:
                application = models.BuildingPermitApplication.objects.get(
                    id=assessment.building_application.id)
                check_if_assessed = models.BuildingDeptAssessment.objects.filter(
                    department=user_department.id,
                    is_active=True,
                    building_application=assessment.building_application.id)
                if len(check_if_assessed) < 1:
                    applications.append(application)
            page = self.paginate_queryset(applications)
            if page is not None:
                serializer = serializers.BuildingApplicationListSerializer(
                    page, many=True)
                return self.get_paginated_response(serializer.data)
        # if first department to assessed
        else:
            querysets = []
            applications = models.BuildingPermitApplication.objects.filter(Q(buildingbasicinformation__reference_number__icontains=search) | Q(buildingdetails__tax_dec_no__icontains=search) | Q(series_number__icontains=search),
                application_status=3)
            for item in applications:
                is_assess = models.BuildingDeptAssessment.objects.filter(
                    building_application=item.id, is_active=True)
                if len(is_assess) < 1:
                    querysets.append(item)
            print(querysets)
            page = self.paginate_queryset(querysets)
            if page is not None:
                serializer = serializers.BuildingApplicationListSerializer(
                    page, many=True)
                return self.get_paginated_response(serializer.data)


class AssessedBusinessApplicationList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def list(self, request):
        search = request.query_params['search']
        user_serializer = serializers.UserSerializer(request.user, many=False)
        user_department = models.Department.objects.get(
            id=user_serializer.data["department"])
        applications = []
        assessed_applications = models.BusinessDeptAssessment.objects.filter(Q(business_application__account_number__icontains=search) | Q(business_application__businessbasicinformation__reference_number__icontains=search) |
                Q(business_application__businessdetails__name__icontains=search) |  Q(business_application__businessdetails__trade_name__icontains=search),
            department=user_department.id).order_by('-updated_at')

        page = self.paginate_queryset(assessed_applications)
        if page is not None:
            serializer = serializers.BusinessDeptAssessmentListSerializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)


class AssessedBuildingApplicationList(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def list(self, request):
        search = request.query_params['search']
        user_serializer = serializers.UserSerializer(request.user, many=False)
        user_department = models.Department.objects.get(
            id=user_serializer.data["department"])
        applications = []
        assessed_applications = models.BuildingDeptAssessment.objects.filter(
            Q(building_application__buildingbasicinformation__reference_number__icontains=search) | Q(building_application__buildingdetails__tax_dec_no__icontains=search) | Q(building_application__series_number__icontains=search),
            department=user_department.id).order_by('-updated_at')

        # for application in assessed_applications:
        #     data = models.BuildingPermitApplication.objects.get(id=application.building_application.id)
        #     applications.append(data)

        page = self.paginate_queryset(assessed_applications)
        if page is not None:
            serializer = serializers.BuildingDeptAssessmentListSerializer(
                page, many=True)
            return self.get_paginated_response(serializer.data)


class SoaListView(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def list(self, request):
        search = request.query_params['search']
        filter = request.query_params['filter']
        soa_list = models.Soa.objects.filter(application_type=filter)
        if filter == 'business' and search != "":
            soa_list = models.Soa.objects.filter(Q(reference_number__icontains=search) | Q(business_application__account_number__icontains=search) | Q(business_application__businessdetails__name__icontains=search) |  Q(business_application__businessdetails__trade_name__icontains=search), application_type=filter)
        elif filter == 'building' and search != "":
            soa_list = models.Soa.objects.filter(Q(reference_number__icontains=search) | Q(building_application__buildingbasicinformation__reference_number__icontains=search), application_type=filter)
        elif filter == 'real_property' and search != "":
            soa_list = models.Soa.objects.filter(Q(reference_number__icontains=search) | Q(building_application__buildingdetails__tax_dec_no=search), application_type=filter)
        page = self.paginate_queryset(soa_list)
        if page is not None:
            serializer = serializers.SoaListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class ResetBusinessAssessment(APIView):
    def put(self, request):
        try:
            business_application = request.data['business_application']
            assessments = models.BusinessDeptAssessment.objects.filter(
                business_application=business_application, is_active=True)
            if len(assessments) > 0:
                for item in assessments:
                    item.is_active = False
                    item.save()
            return Response({"message": "Operation Success!"})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResetBuildingAssessment(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request):
        try:
            building_application = request.data['building_application']
            assessments = models.BuildingDeptAssessment.objects.filter(
                building_application=building_application, is_active=True)
            if len(assessments) > 0:
                for item in assessments:
                    item.is_active = False
                    item.save()
            return Response({"message": "Operation Success!"})
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDepartmentView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            user_serializer = serializers.UserSerializer(request.user,
                                                         many=False)
            user_department = models.Department.objects.get(
                id=user_serializer.data["department"])
            serializer = serializers.DepartmentSerializer(user_department,
                                                          many=False)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BankTransactionListView(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination
    def list(self, request):
        params = request.query_params
        transaction_type = params["type"]
        req_filter = params["filter"]
        search = params["search"]
        if req_filter == "all":
            queryset = self.filter_queryset(
                models.BankTransaction.objects.filter(soa__application_type=transaction_type, reference_no__icontains=search).order_by('-created_at'))
        else:
            is_verified = True if req_filter == "true" else False
            queryset = self.filter_queryset(
                models.BankTransaction.objects.filter(soa__application_type=transaction_type, is_verified =is_verified, reference_no__icontains=search).order_by('-created_at'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.BankTransactionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

class BankTransactionView(APIView):
    pagination_class = BasicPagination
    def get_transaction_obj(self, pk):
        try:
            return models.BankTransaction.objects.get(pk=pk)
        except models.BankTransaction.DoesNotExist:
            raise Http404

    def put(self, request):
        try:
            transaction = self.get_transaction_obj(request.data['id'])
            transaction.is_verified = True
            transaction.payment_receipt = request.data["payment_receipt"]
            transaction.save()
            return Response({
                "code": "ok",
                "message": "Data updated successfully."
            })
        except:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LandBankTransactionView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            payload = {
                "merchant_ref_no": data['MerchantRefNo'],
                "particulars": data["Particulars"],
                "amount": data["Amount"],
                "payor_name": data["PayorName"],
                "payor_email": data["PayorEmail"],
                "status": data["Status"],
                "epp_ref_no": data["EppRefNo"],
                "payment_option": data["PaymentOption"]
            }
            serializer = serializers.LandbankTransactionSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "Ok", "message": "Data successfully created!", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response({"status": "Failed", "message": "Bad Request"},
                        status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return Response(
                {"status": "Failed" ,'message': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LandbankTransactionListView(ListAPIView):
    pagination_class = BasicPagination
    def list(self, request):
        fil = request.query_params['filter']
        search = request.query_params["search"]
        queryset = self.filter_queryset(
            models.LandbankTransaction.objects.filter(merchant_ref_no__application_type=fil, merchant_ref_no__reference_number__icontains=search).order_by('-created_at')
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.LandbankTransactionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

class PisoPayTransactionListView(ListAPIView):
    pagination_class = BasicPagination
    def list(self, request):
        fil = request.query_params["filter"]
        search = request.query_params["search"]
        queryset = self.filter_queryset(models.PisoPayTransaction.objects.filter(trace_number__application_type=fil, trace_number__reference_number__icontains=search).order_by('-created_at'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.PisoPayTransactionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

class VerifySoaPaymentView(APIView):
    permission_classes = [IsAdminUser]

    def get_soa_object(self, pk):
        try:
            return models.Soa.objects.get(pk=pk)
        except models.Soa.DoesNotExist:
            raise Http404
    def put(self, request):
        try:
            id = request.data['id']
            es = SoaEmailService(id)
            soa = self.get_soa_object(id)
            soa.is_verified = True
            soa.save()
            if soa.business_application:
                es.send_business_soa_success()
            else:
                es.send_rpt_soa_success()
            return Response({"status": "Ok", "message": "Soa verified successfully."},
                status=status.HTTP_200_OK)
        except Exception:
            traceback.print_exc()
            return Response(
                {"status": "Failed" ,'message': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class InquiryReport(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        try:
            response = HttpResponse(
                content_type='text/csv',

            )

            writer = csv.writer(response)
            writer.writerow(['Date', 'Total'])
            data = models.Thread.objects.filter(is_remarks=False, is_delinquent=False).annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id'))
            print(data)
            for i in data:
                writer.writerow([i['day'], i['count']])
            return response
        except Exception:
            traceback.print_exc()
            return Response(
                {"status": "Failed" ,'message': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusinessPermitFileView(APIView):
    permission_classes = [IsAdminUser]
    def get_file_obj(self, pk):
        try:
            return models.BusinessPermitFile.objects.get(pk=pk)
        except models.BusinessPermitFile.DoesNotExist:
            raise Http404

    def post(self, request):
        try:
            file_obj = request.FILES['file']
            data = {
                'application_id': request.data['application_id'],
                'filename': request.data['filename']
            }

            serializer = serializers.BusinessPermitFilesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                business_permit = self.get_file_obj(serializer.data['id'])
                update_serializer = serializers.BusinessPermitFilesSerializer(business_permit, request.data)

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

    def get(self, request):
        try:
            application = request.query_params['id']
            data = models.BusinessPermitFile.objects.filter(application_id=application)
            serializer = serializers.BusinessPermitFilesSerializer(data,
                                                                many=True)
            return Response(serializer.data)
        except Exception:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SoaAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get_soa_obj(self, reference_number):
        try:
            return models.Soa.objects.get(reference_number=reference_number)
        except models.Soa.DoesNotExist:
            raise Http404

    def put(self, request):
        try:
            ref_no = request.data['reference_number']
            soa = self.get_soa_obj(ref_no)
            soa.is_verified = True
            soa.save()
            return Response({
                "code": "ok",
                "message": 'Data updated successfully.'
            })
        except:
            traceback.print_exc()
            return Response(
                {'detail': 'Something went wrong. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SoaAPIListView(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = BasicPagination

    def list(self, request):
        search = request.query_params['search']
        filter = request.query_params['filter']
        soa_list = models.Soa.objects.filter(application_type=filter)
        if filter == 'business' and search != "":
            soa_list = models.Soa.objects.filter(Q(reference_number__icontains=search) | Q(business_application__account_number__icontains=search) | Q(business_application__businessdetails__name__icontains=search) |  Q(business_application__businessdetails__trade_name__icontains=search), application_type=filter)
        elif filter == 'building' and search != "":
            soa_list = models.Soa.objects.filter(Q(reference_number__icontains=search) | Q(building_application__buildingbasicinformation__reference_number__icontains=search), application_type=filter)
        elif filter == 'real_property' and search != "":
            soa_list = models.Soa.objects.filter(Q(reference_number__icontains=search) | Q(building_application__buildingdetails__tax_dec_no=search), application_type=filter)
        page = self.paginate_queryset(soa_list)
        if page is not None:
            serializer = serializers.SoaAPIListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)