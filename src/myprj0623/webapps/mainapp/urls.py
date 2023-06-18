"""
URL Configuration for mainapp
"""
from django.urls import path

from . import views
from .constants import const

app_name = 'mainapp'

urlpatterns = [
    path('welcome/', views.WelcomeView.as_view(), name=const.WELCOME_URL_NAME),
    path('home/', views.HomeView.as_view(), name=const.HOME_URL_NAME),
    path("report/search/", views.ReportSearchListView.as_view(), name=const.REPORT_SEARCH_URL_NAME),
    path("report/my_reports/", views.ReportMyReportListView.as_view(), name=const.REPORT_MY_REPORTS_URL_NAME),
    path("report/create/", views.report_create, name=const.REPORT_CREATE_URL_NAME),
    path("report/detail/<int:report_id>/", views.report_detail, name=const.REPORT_DETAIL_URL_NAME),
    path("report/delete/<int:report_id>/", views.report_delete, name=const.REPORT_DELETE_URL_NAME),
]
