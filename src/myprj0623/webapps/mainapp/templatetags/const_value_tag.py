"""
TemplateTag for pagination in mainapp app.
"""

from django import template

from ..constants import const, db_const

register = template.Library()


# !!!IMPORTANT!!!:
#  Display dictionary is only callable from templates using "get_heavy_db_conf_fields_name()" method of
#  template tag (const_value_tag).
#  To call from templates, use django template tag (DO NOT BREAK A LINE IN THE TAG) and write like this:
#    {% get_heavy_db_const_fields_disp_name "{display dictionary name}" {form/record name}.{field_name} as {name} %}
#  Option list info of heavy db const fields should be added to "DISPLAY_DICTINARY_FOR_HEAVY_DB_CONF_FIELDS" following
#  this format: "'{option list name}_DISP_DICT': _convert_option_list_to_dict({option list}),"

def _convert_option_list_to_dict(option_list):
    return {record[0]: record[1] for record in option_list}


DISPLAY_DICTINARY_FOR_HEAVY_DB_CONF_FIELDS = {
    'STATION_LONDON_OPTION_LIST_DISP_DICT': _convert_option_list_to_dict(db_const.STATION_LONDON_OPTION_LIST),
    # (Add next option list disp dict here)
}


@register.simple_tag
def get_const_value(name):
    """
    Return constant value linked to specified name.

    Mainly used for loading constants value in templates.

    :param (str) name: Constant name
    :return: (str) -: Constant value
    """
    return getattr(const, name, "")


@register.simple_tag
def get_heavy_db_const_fields_disp_name(option_list_disp_dict_name, record_key):
    """
    Return heavy DB constant field's name linked to the key in option list display dictionary

    Mainly used for loading heavy DB constants name in templates.

    :param (str) option_list_disp_dict_name: Display dictionary name of Option list (DB constant)
    :param (str) record_key: Key of record (Key of display dictionary)
    :return: (str) -: Constant value
    """
    if option_list_disp_dict_name in DISPLAY_DICTINARY_FOR_HEAVY_DB_CONF_FIELDS and \
            DISPLAY_DICTINARY_FOR_HEAVY_DB_CONF_FIELDS[option_list_disp_dict_name] and \
            record_key in DISPLAY_DICTINARY_FOR_HEAVY_DB_CONF_FIELDS[option_list_disp_dict_name]:
        return DISPLAY_DICTINARY_FOR_HEAVY_DB_CONF_FIELDS[option_list_disp_dict_name][record_key]
    return ""
