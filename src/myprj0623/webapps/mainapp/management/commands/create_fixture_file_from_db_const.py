import os
from datetime import datetime

from django.core.management.base import BaseCommand

from ...constants import const


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Create fixture file from db_const.py by "python manage.py create_fixture_file_from_db_const" command.

        Before running this command, finish migration, create superuser, and set IS_FIXTURE = True on
        core > sesttings > base.py.
        After running this command, reset IS_FIXTURE flg and run "python manage.py loaddata {the fixture file path}"
        :param (Not set (To use optional arguments, define add_arguments() method.))
        :return: (No return)
        """
        path_before_mainapp = "./" if os.getcwd().endswith('webapps') else "./webapps/"
        str_datetime_now = datetime.now().strftime("%m-%d-%Y_%H%M%S")
        path_from_mainapp = 'mainapp/fixture/db_const_fixture_' + str_datetime_now + '.json'
        path = path_before_mainapp + path_from_mainapp
        with open(path, mode='w') as f:
            f.write(const.LIST_START_STR + const.NEW_LINE_STR)
            db_const_table_names_dict_items = const.DB_CONST_TABLE_NAMES_DICT.items()
            for i, (db_const_table_name, db_const_list) in enumerate(db_const_table_names_dict_items):
                db_const_table_name_for_fixture = db_const_table_name.replace(const.UNDERSCORE_STR, const.PERIOD_STR)
                for j, record in enumerate(db_const_list):
                    # Do not add comma to the last element
                    if (i == len(db_const_table_names_dict_items) - 1) and (j == len(db_const_list) - 1):
                        modified_comma = ""
                    else:
                        modified_comma = const.COMMA_WITH_SPACE_STR

                    json_record = \
                        const.INDENT_HALF_STR + const.DICT_START_STR + const.NEW_LINE_STR + \
                        '    "model": "' + \
                        db_const_table_name_for_fixture + \
                        const.DOUBLE_QUOTE_STR + const.COMMA_WITH_SPACE_AND_NEW_LINE_STR + \
                        '    "pk": ' + str(j + 1) + ',\n' + \
                        '    "fields": {\n' + \
                        '      "key": "' + \
                        record[0] + const.DOUBLE_QUOTE_STR + const.COMMA_WITH_SPACE_AND_NEW_LINE_STR + \
                        '      "value": "' + \
                        record[1] + const.DOUBLE_QUOTE_STR + const.COMMA_WITH_SPACE_AND_NEW_LINE_STR + \
                        '      "created_by": 1, \n' + \
                        '      "updated_by": null, \n' + \
                        '      "deleted_by": null, \n' + \
                        '      "created_at": "2023-01-01T00:00:00.000Z", \n' + \
                        '      "updated_at": null, \n' + \
                        '      "deleted_at": null, \n' + \
                        '      "del_flg": false, \n' + \
                        '      "record_updated_by": 1, \n' + \
                        '      "record_updated_at": "2023-01-01T00:00:00.000Z" \n' + \
                        '    }\n' + \
                        const.INDENT_HALF_STR + const.DICT_END_STR + modified_comma + const.NEW_LINE_STR
                    f.write(json_record)
                print(
                    str(len(db_const_list)) + " record(s) data of " + db_const_table_name_for_fixture +
                    " table has written"
                )
            f.write(const.LIST_END_STR + const.NEW_LINE_STR)
            f.close()
        print('FINISHED: Fixture file created to "' + path + const.DOUBLE_QUOTE_STR)
