"""
TemplateTag for pagination in mainapp app.
"""
from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """
    Return url replacing a specified field with a specified value.

    Mainly used for page navigation.

    :param (dict) request: Request
    :param (str) field: The field name in url
    :param (str) value: The string to replace the field (old value) with
    :return: (str) -: Modified url
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
