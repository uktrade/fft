from core.models import FinancialYear
from core.utils.export_helpers import export_to_excel
from core.utils.generic_helpers import (
    get_current_financial_year,
    today_string,
)

from forecast.models import (
    BudgetMonthlyFigure,
)
from forecast.utils.query_fields import (
    ForecastQueryFields,
)


def get_obj_value(obj, name):
    value = 0
    if name in obj:
        value = obj[name]
        if value is None:
            value = 0
    return value


def export_mi_iterator(queryset, fields):
    yield [
        "Entity",
        "Cost Centre",
        "Natural Account",
        "Programme",
        "Analysis",
        "Analysis2",
        "Project",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
        "JAN",
        "FEB",
        "MAR",
        "ADJ01",
        "ADJ02",
        "ADJ03",
        "Total",
    ]
    for obj in queryset:
        apr = get_obj_value(obj, "Apr")
        may = get_obj_value(obj, "May")
        jun = get_obj_value(obj, "Jun")
        jul = get_obj_value(obj, "Jul")
        aug = get_obj_value(obj, "Aug")
        sep = get_obj_value(obj, "Sep")
        oct = get_obj_value(obj, "Oct")
        nov = get_obj_value(obj, "Nov")
        dec = get_obj_value(obj, "Dec")
        jan = get_obj_value(obj, "Jan")
        feb = get_obj_value(obj, "Feb")
        mar = get_obj_value(obj, "Mar")
        adj1 = get_obj_value(obj, "Adj1")
        adj2 = get_obj_value(obj, "Adj2")
        adj3 = get_obj_value(obj, "Adj3")

        total = (
            apr
            + may
            + jun
            + jul
            + aug
            + sep
            + oct
            + nov
            + dec
            + jan
            + feb
            + mar
            + adj1
            + adj2
            + adj3
        )
        yield [
            "3000",
            obj[fields.cost_centre_code_field],
            obj[fields.nac_code_field],
            obj[fields.programme_code_field],
            obj[fields.analysis1_code_field],
            obj[fields.analysis2_code_field],
            obj[fields.project_code_field],
            apr / 100,
            may / 100,
            jun / 100,
            jul / 100,
            aug / 100,
            sep / 100,
            oct / 100,
            nov / 100,
            dec / 100,
            jan / 100,
            feb / 100,
            mar / 100,
            adj1 / 100,
            adj2 / 100,
            adj3 / 100,
            total / 100,
        ]


def create_mi_source_report():
    title = f"MI Report {today_string()}"
    fields = ForecastQueryFields()
    queryset = fields.datamodel.view_data.raw_data_annotated(
        fields.MI_REPORT_DOWNLOAD_COLUMNS
    )
    return export_to_excel(queryset, export_mi_iterator, title, fields)


def create_mi_previous_year_source_report():
    previous_year = get_current_financial_year() - 1
    title = \
        f"MI {FinancialYear.objects.get(pk=previous_year).financial_year_display} " \
        f"Report {today_string()}"
    fields = ForecastQueryFields(previous_year)
    queryset = fields.datamodel.view_data.raw_data_annotated(
        fields.MI_REPORT_DOWNLOAD_COLUMNS, year=previous_year
    )
    return export_to_excel(queryset, export_mi_iterator, title, fields)


def create_mi_budget_report():
    title = f"MI Budget {today_string()}"
    fields = ForecastQueryFields()
    queryset = BudgetMonthlyFigure.pivot.pivot_data(
        fields.MI_REPORT_DOWNLOAD_COLUMNS, {"archived_status__isnull": True}
    )
    return export_to_excel(queryset, export_mi_iterator, title, fields)
