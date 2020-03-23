from core.utils import today_string

from core.exportutils import export_to_excel

from forecast.models import ForecastingDataView
from forecast.utils.query_fields import MI_REPORT_DOWNLOAD_COLUMNS

def export_oscarreport_iterator(queryset):
    yield [
        "Entity",
        "Cost Centre",
        "Natural Account",
        "Programme",
        "Analysis",
        "Analysis2",
        "Spare2",
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
        "Total"
    ]
    for obj in queryset:
        yield [
            "3000",
            obj.financial_code.cost_centre.cost_centre_code,
            obj.financial_code.natural_account_code.natural_account_code,
            obj.financial_code.programme.programme_code,
            obj.financial_code.analysis1_code.analysis1_code,
            obj.financial_code.analysis2_code.analysis2_code,
            obj.project_code.project_code,
            obj.apr,
            obj.may,
            obj.jun,
            obj.jul,
            obj.aug,
            obj.sep,
            obj.oct,
            obj.nov,
            obj.dec,
            obj.jan,
            obj.feb,
            obj.mar,
            obj.adj1,
            obj.adj2,
            obj.adj3,
            obj.apr +
            obj.may +
            obj.jun +
            obj.jul +
            obj.aug +
            obj.sep +
            obj.oct +
            obj.nov +
            obj.dec +
            obj.jan +
            obj.feb +
            obj.mar +
            obj.adj1 +
            obj.adj2  +
            obj.adj3
        ]


def create_mi_source_report():
    title = f'MI Report {today_string()}'
    queryset =  ForecastingDataView.view_data.raw_data_annotated(MI_REPORT_DOWNLOAD_COLUMNS)
    return export_to_excel(queryset, export_oscarreport_iterator, title)
