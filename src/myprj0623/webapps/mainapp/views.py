"""
Views for mainapp
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.views.decorators.http import require_http_methods
from django.views.generic import *

from . import models
from .constants import const, msg_const
from .forms import ReportModelForm, ReportSearchForm
from .models import Report


class WelcomeView(TemplateView):
    template_name = const.WELCOME_TEMPLATE_NAME


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = const.HOME_TEMPLATE_NAME


class ReportSearchListView(LoginRequiredMixin, ListView):
    # !!!IMPORTANT!!!:
    #  Do not use FilterView. It does not work with django bootstrap datepicker, pagination, and crispy form.
    #  You need to filter by date conditions in get_queryset() before filterset being initialized.
    #  For more information, see comments in clean() of ReportSearchForm.
    login_url = settings.LOGIN_URL
    template_name = const.REPORT_SEARCH_TEMPLATE_NAME
    model = models.Report
    paginate_by = const.PAGINATION_MAX
    context_object_name = 'search_result'

    def get_queryset(self):
        """
        Return queryset

        Filter manually according to HttpRequest.

        :param (No param)
        :return: (QuerySet) query_set: Filtered result
        """
        user = self.request.user
        problem_happened_date_min = self.request.GET.get('problem_happened_date_min')
        problem_happened_date_max = self.request.GET.get('problem_happened_date_max')
        postcode = self.request.GET.get('postcode')
        town_city_borough_name = self.request.GET.get('town_city_borough_name')
        nearest_station = self.request.GET.get('nearest_station')
        problem_type = self.request.GET.get('problem_type')
        title = self.request.GET.get('title')

        # Exclude deleted records
        query_set = Report.objects.filter(del_flg=False)

        # Exclude test record if user is not a superuser,
        if user and not user.is_superuser:
            query_set = query_set.filter(test_flg=False)

        # Filter by date conditions before filterset being initialized.
        # (For more information, see comments in clean() of ReportSearchForm.)
        if problem_happened_date_min and problem_happened_date_max:
            query_set = \
                query_set.filter(problem_happened_date__range=[problem_happened_date_min, problem_happened_date_max])
        elif problem_happened_date_min:
            query_set = query_set.filter(problem_happened_date__gte=problem_happened_date_min)
        elif problem_happened_date_max:
            query_set = query_set.filter(problem_happened_date__lte=problem_happened_date_max)

        # Filter by list field
        if town_city_borough_name:
            query_set = query_set.filter(town_city_borough_name=town_city_borough_name)
        if nearest_station:
            query_set = query_set.filter(nearest_station=nearest_station)
        if problem_type:
            query_set = query_set.filter(problem_type=problem_type)

        # Filter by text field
        if postcode:
            query_set = query_set.filter(postcode__icontains=postcode)
        if title:
            query_set = query_set.filter(title__icontains=title)

        return query_set.order_by('-problem_happened_date')

    def get_context_data(self, **kwargs):
        """
        Return context data

        Set form manually.

        :param (No param)
        :return: (dict) context: Context data
        """
        context = super(ReportSearchListView, self).get_context_data(**kwargs)

        # Set previous values into fields
        form = ReportSearchForm()
        for item in form.fields:
            form.fields[item].initial = self.request.GET.get(item)
        context['form'] = form

        return context


class ReportMyReportListView(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    template_name = const.REPORT_MY_REPORTS_TEMPLATE_NAME
    model = models.Report
    paginate_by = const.PAGINATION_MAX
    context_object_name = 'search_result'

    def get_queryset(self):
        return Report.objects.filter(created_by=self.request.user).filter(del_flg=False) \
            .order_by('-problem_happened_date')


@login_required
def report_create(request):
    template_name = const.REPORT_CREATE_DETAIL_TEMPLATE_NAME
    user = request.user

    if request.POST:
        # Create new record by requested data
        report_form = ReportModelForm(data=request.POST, user=user)
        if report_form.is_valid():
            new_record = Report.exec_create(request, report_form)
            report_id = new_record.id
            messages.add_message(
                request, messages.SUCCESS,
                _get_report_success_msg(const.ACTION_TYPE_CREATE, report_id)
            )
            return redirect(const.REPORT_DETAIL_PAGE_NAME, str(report_id))
    else:
        # Initialize by no data
        report_form = ReportModelForm(user=user)

    context = {
        'report_form': report_form,
    }
    return render(request, template_name, context)


@login_required
def report_detail(request, report_id):
    template_name = const.REPORT_CREATE_DETAIL_TEMPLATE_NAME
    user = request.user
    target_report = get_object_or_404(Report, id=report_id)

    if target_report.del_flg:
        messages.add_message(
            request, messages.ERROR, msg_const.ALREADY_DELETED_MESSAGE
        )
        return redirect(const.REPORT_SEARCH_PAGE_NAME)

    if request.POST:
        # Update target record by requested data
        report_form = ReportModelForm(data=request.POST, user=user, instance=target_report)
        if report_form.is_valid():
            target_report.exec_update(request, report_form)
            report_id_str = str(report_id)
            messages.add_message(
                request, messages.SUCCESS,
                _get_report_success_msg(const.ACTION_TYPE_UPDATE, report_id)
            )
            return redirect(const.REPORT_DETAIL_PAGE_NAME, report_id_str)
    else:
        # Initialize by target record
        report_form = ReportModelForm(user=user, instance=target_report)

    context = {
        'report_form': report_form,
        'is_detail': True,
        'target_report': target_report,
    }
    return render(request, template_name, context)


@login_required
@require_http_methods(["POST"])
def report_delete(request, report_id):
    target_report = get_object_or_404(Report, id=report_id)
    if target_report.del_flg:
        messages.add_message(
            request, messages.ERROR, msg_const.ALREADY_DELETED_MESSAGE
        )
    else:
        # Logically delete target record by requested data
        target_report.exec_delete(request)
        messages.add_message(
            request, messages.SUCCESS,
            _get_report_success_msg(const.ACTION_TYPE_DELETE, report_id)
        )
    return redirect(const.REPORT_SEARCH_PAGE_NAME)


def _get_report_success_msg(action_str, report_id):
    """
    Return success message for Report (create, update, delete)

    :param (str) action_str: Action name
    :param (int) report_id: report.id
    :return: (str)-: Success message
    """
    if action_str == const.ACTION_TYPE_CREATE:
        action_msg = "Created"
    elif action_str == const.ACTION_TYPE_UPDATE:
        action_msg = "Updated"
    else:
        action_msg = "Deleted"

    return "Report " + action_msg + " (Report No. " + str(report_id) + ")"
