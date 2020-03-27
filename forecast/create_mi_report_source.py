from core.exportutils import export_to_excel
from core.utils import today_string

from forecast.models import ForecastingDataView
from forecast.utils.query_fields import (
    ANALYSIS1_CODE,
    ANALYSIS2_CODE,
    COST_CENTRE_CODE,
    MI_REPORT_DOWNLOAD_COLUMNS,
    NAC_CODE,
    PROGRAMME_CODE,
    PROJECT_CODE,
)


def export_oscarreport_iterator(queryset):
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
        yield [
            "3000",
            obj[COST_CENTRE_CODE],
            obj[NAC_CODE],
            obj[PROGRAMME_CODE],
            obj[ANALYSIS1_CODE],
            obj[ANALYSIS2_CODE],
            obj[PROJECT_CODE],
            obj["Apr"] / 100,
            obj["May"] / 100,
            obj["Jun"] / 100,
            obj["Jul"] / 100,
            obj["Aug"] / 100,
            obj["Sep"] / 100,
            obj["Oct"] / 100,
            obj["Nov"] / 100,
            obj["Dec"] / 100,
            obj["Jan"] / 100,
            obj["Feb"] / 100,
            obj["Mar"] / 100,
            obj["Adj1"] / 100,
            obj["Adj2"] / 100,
            obj["Adj3"] / 100,
            (
                obj["Apr"]
                + obj["May"]
                + obj["Jun"]
                + obj["Jul"]
                + obj["Aug"]
                + obj["Sep"]
                + obj["Oct"]
                + obj["Nov"]
                + obj["Dec"]
                + obj["Jan"]
                + obj["Feb"]
                + obj["Mar"]
                + obj["Adj1"]
                + obj["Adj2"]
                + obj["Adj3"]
            )
            / 100,
        ]


def create_mi_source_report():
    title = f"MI Report {today_string()}"
    queryset = ForecastingDataView.view_data.raw_data_annotated(
        MI_REPORT_DOWNLOAD_COLUMNS
    )
    return export_to_excel(queryset, export_oscarreport_iterator, title)
