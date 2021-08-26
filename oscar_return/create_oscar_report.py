from django.db.models import Q

from core.models import FinancialYear
from core.utils.export_helpers import export_to_excel
from core.utils.generic_helpers import (
    get_current_financial_year,
    today_string,
)

from oscar_return.models import (
    HistoricOSCARReturn,
    OSCARReturn,
)


def export_oscarreport_iterator(queryset):
    yield [
        "Row",
        "Organisation",
        "Organisation Alias",
        "COA",
        "COA Alias",
        "Sub Segment",
        "Sub Segment Alias",
        "Adj Type",
        "AdjType Alias",
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
    ]
    for obj in queryset:
        try:
            yield [
                obj.row_number,
                obj.organization_code,
                obj.organization_alias,
                obj.account_l5_code.account_l5_code if obj.account_l5_code else "",
                obj.account_l5_code.account_l5_long_name if obj.account_l5_code else "",
                obj.sub_segment_code,
                obj.sub_segment_long_name,
                "TYPE_INYEAR",
                "IN-YEAR RETURN",
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
                (obj.mar if obj.mar else 0)
                + (obj.adj1 if obj.adj1 else 0)
                + (obj.adj2 if obj.adj2 else 0)
                + (obj.adj3 if obj.adj3 else 0),
            ]
        except OSCARReturn.account_l5_code.RelatedObjectDoesNotExist:
            pass


def create_oscar_report():
    current_year = get_current_financial_year()
    title = (
        f"OSCAR {FinancialYear.objects.get(pk=current_year).financial_year_display} "
        f" {today_string()}"
    )
    queryset = OSCARReturn.objects.all()
    return export_to_excel(queryset, export_oscarreport_iterator, title)


def create_previous_year_oscar_report():
    previous_year = get_current_financial_year() - 1
    title = (
        f"OSCAR {FinancialYear.objects.get(pk=previous_year).financial_year_display} "
        f" {today_string()}"
    )
    queryset = HistoricOSCARReturn.objects.filter(financial_year=previous_year).exclude(
        Q(apr=0)
        & Q(may=0)
        & Q(jun=0)
        & Q(jul=0)
        & Q(aug=0)
        & Q(sep=0)
        & Q(oct=0)
        & Q(nov=0)
        & Q(dec=0)
        & Q(jan=0)
        & Q(feb=0)
        & Q(mar=0)
        & Q(adj1=0)
        & Q(adj2=0)
        & Q(adj3=0)
    )
    return export_to_excel(queryset, export_oscarreport_iterator, title)
