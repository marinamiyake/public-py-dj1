"""
Forms for mainapp
"""
from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Layout, Submit
from django import forms

from . import models
from .constants import const, css_const, db_const


class CustomDateInput(forms.DateInput):
    input_type = 'date'


class ReportModelForm(forms.ModelForm):
    # Set choices (option list) for heavy db conf fields
    nearest_station = forms.ChoiceField(
        label=const.NEAREST_STATION_VERBOSE_NAME,
        choices=const.CHOICE_UNSELECTED_LIST + db_const.STATION_LONDON_OPTION_LIST,
    )

    # Other changes
    postcode = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g. SW1A1AA'})
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        data_area = Div(
            # Smartphone: default(max12 row1), Tablet: width6(row1-1st), Desktop: default(width6 row1-1st)
            Div(
                Div(
                    'problem_happened_date',
                    css_class=css_const.CSS_CLASS_SEPARATOR.join(
                        [css_const.CSS_TABLET_COL_6, css_const.CSS_DESKTOP_COL_3])
                ),
                css_class='row'
            ),
            # Smartphone: default(max12 row2), Tablet: width4(row2-1st), Desktop: width2(row2-1st)
            Div(
                'postcode',
                css_class=css_const.CSS_CLASS_SEPARATOR.join([css_const.CSS_TABLET_COL_6, css_const.CSS_DESKTOP_COL_3])
            ),
            # Smartphone: default(max12 row3), Tablet: width8(row2-2nd), Desktop: width4(row2-2nd)
            Div(
                'town_city_borough_name',
                css_class=css_const.CSS_CLASS_SEPARATOR.join([css_const.CSS_TABLET_COL_6, css_const.CSS_DESKTOP_COL_4])
            ),
            # Smartphone: default(max12 row4), Tablet: default(max12 row3), Desktop: width6(row2-3rd)
            Div('nearest_station', css_class=css_const.CSS_DESKTOP_COL_5),
            # Smartphone: default(max12 row5), Tablet: default(max12 row4), Desktop: width6(row3)
            Div('address_line', css_class=css_const.CSS_ALL_COL_MAX_12),
            # Smartphone: width12(row6), Tablet: default(same as smartphone row5), Desktop: default(same as tablet row4)
            Div('problem_type', css_class=css_const.CSS_CLASS_SEPARATOR.join(
                [css_const.CSS_TABLET_COL_6, css_const.CSS_DESKTOP_COL_3])
                ),
            # Smartphone: width12(row7), Tablet: default(same as smartphone row6), Desktop: default(same as tablet row5)
            Div('title', css_class=css_const.CSS_ALL_COL_MAX_12),
            # Smartphone: width12(row8), Tablet: default(same as smartphone row7), Desktop: default(same as tablet row6)
            Div('detail', css_class=css_const.CSS_ALL_COL_MAX_12),
            css_class='row'
        )
        # If accessed via detail (read/update) URL
        report_id = self.instance.pk
        if report_id:
            report_id_title = HTML('<h2 class="py-2" style="font-size:20px">Report No. {{ target_report.id }}</h2>')
            # Editable only for superusers and created user
            if user.is_superuser or user.id == self.instance.created_by.id:
                self.helper.layout = Layout(
                    report_id_title,
                    data_area,
                    Div(
                        HTML('''
                                <button type="button" class="btn btn-danger me-2" data-bs-toggle="modal" 
                                data-bs-target="#reportDeleteModal-''' + str(report_id) + '''">Delete</button>
                            '''),
                        Submit('submit', "Update", css_class='btn-success ml-auto'),
                        HTML('</div>'),
                        css_class='d-flex justify-content-end'
                    ),
                )
            else:
                for disabled_field_name in self.base_fields.keys():
                    self.fields[disabled_field_name].disabled = True
                self.helper.layout = Layout(
                    report_id_title,
                    data_area,
                )

        # If accessed via create URL
        else:
            self.helper.layout = Layout(
                data_area,
                Div(
                    Submit('submit', "Create", css_class='btn-success'),
                    css_class='d-flex justify-content-end'
                ),
            )

    class Meta:
        model = models.Report
        fields = (
            "postcode",
            "town_city_borough_name",
            "address_line",
            "nearest_station",
            "problem_type",
            "problem_happened_date",
            "title",
            "detail",
        )
        widgets = {
            "problem_happened_date": DatePickerInput(),
        }
        labels = {
            "postcode": const.POSTCODE_VERBOSE_NAME,
            "town_city_borough_name": const.TOWN_CITY_BOROUGH_NAME,
            "address_line": const.ADDRESS_LINE_VERBOSE_NAME,
            "nearest_station": const.NEAREST_STATION_VERBOSE_NAME,
            "problem_type": const.PROBLEM_TYPE_VERBOSE_NAME,
            "problem_happened_date": const.PROBLEM_HAPPENED_DATE_VERBOSE_NAME,
            "title": const.TITLE_VERBOSE_NAME,
            "detail": const.DETAIL_VERBOSE_NAME,
        }


class ReportSearchForm(forms.Form):
    problem_happened_date_min = forms.DateField(
        label=const.PROBLEM_HAPPENED_DATE_VERBOSE_NAME + " (From)",
        widget=DatePickerInput(),
        required=False,
    )
    problem_happened_date_max = forms.DateField(
        label=const.PROBLEM_HAPPENED_DATE_VERBOSE_NAME + " (To)",
        widget=DatePickerInput(range_from="problem_happened_date_min"),
        required=False
    )
    postcode = forms.CharField(
        label=const.POSTCODE_VERBOSE_NAME,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. SW1A1AA'}),
        required=False
    )
    town_city_borough_name = forms.ChoiceField(
        label=const.TOWN_CITY_BOROUGH_NAME,
        choices=const.CHOICE_UNSELECTED_LIST + db_const.TOWN_CITY_BOROUGH_NAME_LONDON_OPTION_LIST,
        required=False,
    )
    nearest_station = forms.ChoiceField(
        label=const.NEAREST_STATION_VERBOSE_NAME,
        choices=const.CHOICE_UNSELECTED_LIST + db_const.STATION_LONDON_OPTION_LIST,
        required=False
    )
    problem_type = forms.ChoiceField(
        label=const.PROBLEM_TYPE_VERBOSE_NAME,
        choices=const.CHOICE_UNSELECTED_LIST + const.PROBLEM_TYPE_LIST,
        required=False
    )
    title = forms.CharField(
        label=const.TITLE_VERBOSE_NAME,
        required=False
    )
    address_line = forms.CharField(
        label=const.ADDRESS_LINE_VERBOSE_NAME,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        data_area = Div(
            # Smartphone: default(max12 row1), Tablet: default(max12 row1), Desktop: width3(row1-1st)
            Div('problem_happened_date_min', css_class=css_const.CSS_DESKTOP_COL_3),
            # Smartphone: default(max12 row2), Tablet: default(max12 row2), Desktop: width3(row1-2nd)
            Div('problem_happened_date_max', css_class=css_const.CSS_DESKTOP_COL_3),
            # Smartphone: default(max12 row3), Tablet: width4(row2-1st), Desktop: width2(row1-3rd)
            Div(
                'postcode',
                css_class=css_const.CSS_CLASS_SEPARATOR.join([css_const.CSS_TABLET_COL_4, css_const.CSS_DESKTOP_COL_2])
            ),
            # Smartphone: default(max12 row4), Tablet: width8(row2-2nd), Desktop: width4(row1-4th)
            Div(
                'town_city_borough_name',
                css_class=css_const.CSS_CLASS_SEPARATOR.join([css_const.CSS_TABLET_COL_8, css_const.CSS_DESKTOP_COL_4])
            ),
            # Smartphone: default(max12 row5), Tablet: default(max12 row3), Desktop: width6(row2-1st)
            Div('nearest_station', css_class=css_const.CSS_DESKTOP_COL_6),
            # Smartphone: default(max12 row6), Tablet: default(max12 row4), Desktop: width6(row2-2nd)
            Div('address_line', css_class=css_const.CSS_DESKTOP_COL_6),
            # Smartphone: default(max12 row7), Tablet: default(max12 row5), Desktop: width6(row3-1st)
            Div('problem_type', css_class=css_const.CSS_DESKTOP_COL_6),
            # Smartphone: default(max12 row8), Tablet: default(max12 row6), Desktop: width6(row3-2nd)
            Div('title', css_class=css_const.CSS_DESKTOP_COL_6),
            css_class='row'
        )
        self.helper.layout = Layout(
            Div(
                Div(
                    data_area,
                    Div(
                        HTML('''
                            <a class="btn btn-outline-secondary me-2" href="{% url 'mainapp:report_search' %}">Reset</a>
                        '''),
                        Submit('submit', "Search", css_class='ml-auto'),
                        HTML('</div>'),
                        css_class='d-flex justify-content-end'
                    ),
                    css_class="row p-4"
                ),
                css_class="border border"
            )
        )
        self.helper.form_method = "GET"
