"""
Models for mainapp
"""
import datetime

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from .constants import const


# ==================================================
# !!!IMPORTANT!!!:
#  Models for generating constants.
#  These models must contain key and value field.
#  Before adding new DB constants, check comments in db_const.py, apps.py, create_db_const_file.py, const_value_tag.py.
#  You cannot use DB constants for model's choices because migration cannot detect DB record (constants) update.
#  You can set DB constants models for ForeignKey, but it may make system heavy if there are huge amount of records and
#  you use it for user updatable field.
#  Please consider to set character field for model's field and override choices in forms.
#  You can get display value from template by calling get_heavy_db_const_fields_disp_name().
# ==================================================

class TownCityBoroughNameLondon(models.Model):
    key = models.CharField(
        max_length=2,
    )
    value = models.CharField(
        max_length=50,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=
        const.TOWN_CITY_BOROUGH_NAME_LONDON_OPTION_LIST_MODEL_VAR_NAME + const.CREATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.CREATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name=
        const.TOWN_CITY_BOROUGH_NAME_LONDON_OPTION_LIST_MODEL_VAR_NAME + const.UPDATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.UPDATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name=
        const.TOWN_CITY_BOROUGH_NAME_LONDON_OPTION_LIST_MODEL_VAR_NAME + const.DELETED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.DELETED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=const.CREATED_AT_VERBOSE_NAME,
    )
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=const.UPDATED_AT_VERBOSE_NAME,
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=const.DELETED_AT_VERBOSE_NAME,
    )
    del_flg = models.BooleanField(
        default=False,
        verbose_name=const.DEL_FLG_VERBOSE_NAME,
    )
    record_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=
        const.TOWN_CITY_BOROUGH_NAME_LONDON_OPTION_LIST_MODEL_VAR_NAME + const.RECORD_UPDATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.RECORD_UPDATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    record_updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=const.RECORD_UPDATED_AT_VERBOSE_NAME,
    )

    def __str__(self):
        return self.value


class StationLondon(models.Model):
    key = models.CharField(
        max_length=6,
    )
    value = models.CharField(
        max_length=50,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=const.STATION_LONDON_OPTION_LIST_MODEL_VAR_NAME + const.CREATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.CREATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name=const.STATION_LONDON_OPTION_LIST_MODEL_VAR_NAME + const.UPDATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.UPDATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name=const.STATION_LONDON_OPTION_LIST_MODEL_VAR_NAME + const.DELETED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.DELETED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=const.CREATED_AT_VERBOSE_NAME,
    )
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=const.UPDATED_AT_VERBOSE_NAME,
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=const.DELETED_AT_VERBOSE_NAME,
    )
    del_flg = models.BooleanField(
        default=False,
        verbose_name=const.DEL_FLG_VERBOSE_NAME,
    )
    record_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=const.STATION_LONDON_OPTION_LIST_MODEL_VAR_NAME + const.RECORD_UPDATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.RECORD_UPDATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    record_updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=const.RECORD_UPDATED_AT_VERBOSE_NAME,
    )

    def __str__(self):
        return self.value


# (Add next model for generating db constants here)

# ==================================================
# ==================================================
# mainapp models
# ==================================================
class Report(models.Model):
    problem_happened_date = models.DateField(
        verbose_name=const.PROBLEM_HAPPENED_DATE_VERBOSE_NAME,
    )
    postcode_format_msg = "Enter capital alphabets or numbers without space."
    postcode = models.CharField(
        max_length=7,
        verbose_name=const.POSTCODE_VERBOSE_NAME,
        help_text=postcode_format_msg,
        validators=[RegexValidator(
            regex="^([A-Z0-9]{5,7})$",
            message=postcode_format_msg
        )]
    )
    town_city_borough_name = models.ForeignKey(
        TownCityBoroughNameLondon,
        related_name=const.REPORT_MODEL_VAR_NAME + const.TOWN_CITY_BOROUGH_NAME_LONDON_OPTION_LIST_MODEL_VAR_NAME,
        verbose_name=const.TOWN_CITY_BOROUGH_NAME,
        on_delete=models.PROTECT,
    )
    # HEAVY DB CONF FIELD: Report.nearest_station
    nearest_station = models.CharField(
        max_length=6,
        verbose_name=const.NEAREST_STATION_VERBOSE_NAME,
    )
    # nearest_station = models.ForeignKey(
    #     StationLondon,
    #     related_name=const.REPORT_MODEL_VAR_NAME + const.STATION_LONDON_OPTION_LIST_MODEL_VAR_NAME,
    #     verbose_name=const.NEAREST_STATION_VERBOSE_NAME,
    #     on_delete=models.PROTECT,
    # )
    address_line = models.CharField(
        max_length=200,
        verbose_name=const.ADDRESS_LINE_VERBOSE_NAME,
    )
    # NOTE: Currently we only support for London, but might enhance function for all cities in the UK in the future.
    county = models.CharField(
        max_length=20,
        default='Greater London',
        verbose_name=const.COUNTY_VERBOSE_NAME,
    )
    problem_type = models.CharField(
        max_length=2,
        choices=const.PROBLEM_TYPE_LIST,
        verbose_name=const.PROBLEM_TYPE_VERBOSE_NAME,
    )
    title = models.CharField(
        max_length=200,
        verbose_name=const.TITLE_VERBOSE_NAME,
    )
    detail = models.TextField(
        max_length=1000,
        verbose_name=const.DETAIL_VERBOSE_NAME,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=const.REPORT_MODEL_VAR_NAME + const.CREATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.CREATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name=const.REPORT_MODEL_VAR_NAME + const.UPDATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.UPDATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name=const.REPORT_MODEL_VAR_NAME + const.DELETED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.DELETED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=const.CREATED_AT_VERBOSE_NAME,
    )
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=const.UPDATED_AT_VERBOSE_NAME,
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=const.DELETED_AT_VERBOSE_NAME,
    )
    del_flg = models.BooleanField(
        default=False,
        verbose_name=const.DEL_FLG_VERBOSE_NAME,
    )
    # ----- Columns for maintenance -----
    record_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name=const.REPORT_MODEL_VAR_NAME + const.RECORD_UPDATED_BY_RELATED_NAME_SUFFIX,
        verbose_name=const.RECORD_UPDATED_BY_VERBOSE_NAME,
        on_delete=models.PROTECT,
    )
    record_updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=const.RECORD_UPDATED_AT_VERBOSE_NAME,
    )
    test_flg = models.BooleanField(
        default=False,
        verbose_name=const.TEST_FLG_VERBOSE_NAME,
    )

    # ----------

    @staticmethod
    def exec_create(request, report_form):
        exec_user = request.user
        new_record = Report(
            postcode=report_form.cleaned_data["postcode"],
            town_city_borough_name=report_form.cleaned_data["town_city_borough_name"],
            address_line=report_form.cleaned_data["address_line"],
            nearest_station=report_form.cleaned_data["nearest_station"],
            problem_type=report_form.cleaned_data["problem_type"],
            problem_happened_date=report_form.cleaned_data["problem_happened_date"],
            title=report_form.cleaned_data["title"],
            detail=report_form.cleaned_data["detail"],
            created_by=exec_user,
            record_updated_by=exec_user,
        )
        new_record.save()
        return new_record

    def exec_update(self, request, report_form):
        exec_user = request.user
        datetime_now = datetime.datetime.now()
        self.postcode = report_form.cleaned_data["postcode"]
        self.town_city_borough_name = report_form.cleaned_data["town_city_borough_name"]
        self.address_line = report_form.cleaned_data["address_line"]
        self.nearest_station = report_form.cleaned_data["nearest_station"]
        self.problem_type = report_form.cleaned_data["problem_type"]
        self.title = report_form.cleaned_data["title"]
        self.detail = report_form.cleaned_data["detail"]
        self.updated_by = exec_user
        self.updated_at = datetime_now
        self.record_updated_by = exec_user
        self.save()

    def exec_delete(self, request):
        exec_user = request.user
        datetime_now = datetime.datetime.now()
        self.deleted_by = exec_user
        self.deleted_at = datetime_now
        self.del_flg = True
        self.record_updated_by = exec_user
        self.save()

# ==================================================
