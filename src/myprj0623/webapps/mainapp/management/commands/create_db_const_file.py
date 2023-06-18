import os
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import connection

from ...constants import const
from ...models import (
    StationLondon,
    TownCityBoroughNameLondon
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Initialize DB constants

        This custom command shall be called from ready() method in mainapp > apps.py

        :param (Not set (To use optional arguments, define add_arguments() method.))
        :return: (No return)
        """
        # Check if first migration is finished (all DB const tables are created)
        if len(set(const.DB_CONST_TABLE_NAMES) - set(connection.introspection.table_names())) == 0:
            _initialize_db_const()
            print("FINISHED: _initialize_db_const()")
        else:
            print("SKIP: _initialize_db_const()")


def _initialize_db_const():
    """
    !!!IMPORTANT!!!: Initialize DB constants

    See comment in mainapp > constants > db_const.py

    :param (No param)
    :return: (No return)
    """
    db_const_dict = {
        'TOWN_CITY_BOROUGH_NAME_LONDON_OPTION_LIST': TownCityBoroughNameLondon.objects.filter(del_flg=False),
        'STATION_LONDON_OPTION_LIST': StationLondon.objects.filter(del_flg=False),
        # (Add next db constant here)
    }

    path_before_mainapp = "./" if os.getcwd().endswith('webapps') else "./webapps/"
    path_from_mainapp = 'mainapp/constants/db_const.py'
    path = path_before_mainapp + path_from_mainapp

    with open(path, mode='w') as f:
        # Clear old info
        f.truncate(0)
        # Write new info
        f.write(
            "# ==================================================\n" +
            "# DB CONSTANTS for main app \n# (Generated by 'python manage.py create_db_const_file' command on " +
            datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ")\n" +
            "# ==================================================\n"
        )
        for db_const_dict_key, db_const_dict_value in db_const_dict.items():
            f.write(db_const_dict_key + const.EQUAL_WITH_SPACE_STR + const.LIST_START_STR + const.NEW_LINE_STR)
            for record in db_const_dict_value:
                f.write(
                    const.INDENT_STR + const.TUPLE_START_STR + const.DOUBLE_QUOTE_STR + record.key +
                    const.DOUBLE_QUOTE_STR + const.COMMA_WITH_SPACE_STR +
                    const.DOUBLE_QUOTE_STR + record.value + const.DOUBLE_QUOTE_STR + const.TUPLE_END_STR +
                    const.COMMA_WITH_SPACE_STR + const.NEW_LINE_STR
                )
            f.write(const.LIST_END_STR + const.NEW_LINE_STR + const.NEW_LINE_STR)
        f.write('# ==================================================\n')
        f.close()