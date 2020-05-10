from core.exportutils import export_to_excel
from core.utils import today_string

from forecast.models import (
    BudgetMonthlyFigure,
    ForecastingDataView,
)
from forecast.utils.query_fields import (
    ANALYSIS1_CODE,
    ANALYSIS2_CODE,
    COST_CENTRE_CODE,
    MI_REPORT_DOWNLOAD_COLUMNS,
    NAC_CODE,
    PROGRAMME_CODE,
    PROJECT_CODE,
)


def export_mi_iterator(queryset):
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
        apr = obj["Apr"] if "Apr" in obj else 0
        may = obj["May"] if "May" in obj else 0
        jun = obj["Jun"] if "Jun" in obj else 0
        jul = obj["Jul"] if "Jul" in obj else 0
        aug = obj["Aug"] if "Aug" in obj else 0
        sep = obj["Sep"] if "Sep" in obj else 0
        oct = obj["Oct"] if "Oct" in obj else 0
        nov = obj["Nov"] if "Nov" in obj else 0
        dec = obj["Dec"] if "Dec" in obj else 0
        jan = obj["Jan"] if "Jan" in obj else 0
        feb = obj["Feb"] if "Feb" in obj else 0
        mar = obj["Mar"] if "Mar" in obj else 0
        adj1 = obj["Adj1"] if "Adj1" in obj else 0
        adj2 = obj["Adj2"] if "Adj2" in obj else 0
        adj3 = obj["Adj3"] if "Adj3" in obj else 0

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
            obj[COST_CENTRE_CODE],
            obj[NAC_CODE],
            obj[PROGRAMME_CODE],
            obj[ANALYSIS1_CODE],
            obj[ANALYSIS2_CODE],
            obj[PROJECT_CODE],
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
    queryset = ForecastingDataView.view_data.raw_data_annotated(
        MI_REPORT_DOWNLOAD_COLUMNS
    )
    return export_to_excel(queryset, export_mi_iterator, title)


def create_mi_budget_report():
    title = f"MI Budget {today_string()}"
    queryset = BudgetMonthlyFigure.pivot.pivot_data(
        MI_REPORT_DOWNLOAD_COLUMNS, {"archived_status__isnull": True}
    )
    return export_to_excel(queryset, export_mi_iterator, title)
