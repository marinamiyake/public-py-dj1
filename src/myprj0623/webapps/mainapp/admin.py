"""
DjangoAdmin settings for mainapp
"""
from django.contrib import admin

from .constants import const
from .models import (Report, StationLondon, TownCityBoroughNameLondon)


class ReportModelAdmin(admin.ModelAdmin):
    disp_fields = [
        "id",
        "del_flg",  # Changed position
        "test_flg",  # Changed position
        "problem_happened_date",
        "postcode",
        "town_city_borough_name",
        "nearest_station",
        "address_line",
        # "county",  # -> Currently not using column (See note in models.py)
        "problem_type",
        "title",
        "detail",
        "created_by",
        "updated_by",
        "deleted_by",
        "created_at",
        "updated_at",
        "deleted_at",
        # "del_flg",  # -> Changed position
        # "record_updated_by",  # -> Subordinate info for specific management
        # "record_updated_at",  # -> Subordinate info for specific management
        # "test_flg",  # -> Changed position
    ]
    save_on_top = True
    save_as = True
    list_display = disp_fields
    date_hierarchy = "created_at"
    search_fields = ('id', 'title')
    list_filter = (
        'del_flg',
    )
    sortable_by = disp_fields
    readonly_fields = [
        'created_at',
        'record_updated_at',
    ]


admin.site.register(Report, ReportModelAdmin)


class TownCityBoroughNameLondonModelAdmin(admin.ModelAdmin):
    list_per_page = const.LIST_PER_PAGE_FOR_DB_CONST_OPTION_LIST
    save_on_top = const.SAVE_ON_TOP_FOR_DB_CONST_OPTION_LIST
    save_as = const.SAVE_AS_FOR_DB_CONST_OPTION_LIST
    list_display = const.LIST_DISPLAY_FIELDS_FOR_DB_CONST_OPTION_LIST
    date_hierarchy = const.DATE_HIERARCHY_FOR_DB_CONST_OPTION_LIST
    search_fields = const.SEARCH_FIELDS_FOR_DB_CONST_OPTION_LIST
    list_filter = const.LIST_FILTER_FOR_DB_CONST_OPTION_LIST
    sortable_by = const.SORTABLE_BY_FOR_DB_CONST_OPTION_LIST
    readonly_fields = const.READONLY_FIELDS_FOR_DB_CONST_OPTION_LIST


admin.site.register(TownCityBoroughNameLondon, TownCityBoroughNameLondonModelAdmin)


class StationLondonModelAdmin(admin.ModelAdmin):
    list_per_page = const.LIST_PER_PAGE_FOR_DB_CONST_OPTION_LIST
    save_on_top = const.SAVE_ON_TOP_FOR_DB_CONST_OPTION_LIST
    save_as = const.SAVE_AS_FOR_DB_CONST_OPTION_LIST
    list_display = const.LIST_DISPLAY_FIELDS_FOR_DB_CONST_OPTION_LIST
    date_hierarchy = const.DATE_HIERARCHY_FOR_DB_CONST_OPTION_LIST
    search_fields = const.SEARCH_FIELDS_FOR_DB_CONST_OPTION_LIST
    list_filter = const.LIST_FILTER_FOR_DB_CONST_OPTION_LIST
    sortable_by = const.SORTABLE_BY_FOR_DB_CONST_OPTION_LIST
    readonly_fields = const.READONLY_FIELDS_FOR_DB_CONST_OPTION_LIST


admin.site.register(StationLondon, StationLondonModelAdmin)
