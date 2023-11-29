from django.urls import path, include
from staff import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'department', views.DepartmentViewSet)
urlpatterns = [
    path('business-permit-application-list/',views.BusinessApplicationList.as_view()),
    path('building-permit-application-list/',views.BuildingApplicationList.as_view()),
    path('business-permit-application/',views.BusinessPermitApplicationView.as_view()),
    path('building-permit-application/',views.BuildingPermitApplicationView.as_view()),
    path('dashboard/',views.DashboardView.as_view()),
    path('threads/', views.ThreadList.as_view()),
    path('remarks-threads/', views.RemarksThreadList.as_view()),
    path('thread/', views.ThreadRespondView.as_view()),
    path('group/', views.VerifyGroupView.as_view()),
    path('appointment-limit-list/', views.AppointmentLimitList.as_view()),
    path('appointment-limit/', views.AppointmentLimitView.as_view()),
    path('appointment-list/', views.AdminAppointmentList.as_view()),
    path('viewsets/', include(router.urls)),
    path('department-list', views.DepartmentList.as_view()),
    path('business-dept-assessment', views.BusinessDeptAssessmentView.as_view()),
    path('building-dept-assessment', views.BuildingDeptAssessmentView.as_view()),
    path('check-business-dept-if-can-assess', views.CheckBusinessDeptIfCanAssess.as_view()),
    path('check-building-dept-if-can-assess', views.CheckBuildingDeptIfCanAssess.as_view()),
    path('for-business-assessment-list', views.ForBusinessAssessmentList.as_view()),
    path('for-building-assessment-list', views.ForBuildingAssessmentList.as_view()),
    path('assessed-business-application-list', views.AssessedBusinessApplicationList.as_view()),
    path('assessed-building-application-list', views.AssessedBuildingApplicationList.as_view()),
    path('reset-business-assessment', views.ResetBusinessAssessment.as_view()),
    path('reset-building-assessment', views.ResetBuildingAssessment.as_view()),
    path('user-department', views.UserDepartmentView.as_view()),
    path('soa-list/', views.SoaListView.as_view()),
    path('bank-transaction-list/', views.BankTransactionListView.as_view()),
    path('bank-transaction/', views.BankTransactionView.as_view()),
    path('delinquent-payments/', views.DelinquentThreadList.as_view()),
    path('landbank-transaction/', views.LandBankTransactionView.as_view()),
    path('landbank-transaction-list/', views.LandbankTransactionListView.as_view()),
    path('pisopay-transaction-list/', views.PisoPayTransactionListView.as_view()),
    path('verify-soa-payment/', views.VerifySoaPaymentView.as_view()),
    path('inquiry-report/', views.InquiryReport.as_view()),
    path('business-permit/', views.BusinessPermitFileView.as_view()),
    path('soa/verify/', views.SoaAPIView.as_view()),
    path('soa/list', views.SoaAPIListView.as_view())
]