import csv

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)

from core.import_csv import (
    ImportInfo,
    csv_header_to_dict,
    get_fk,
    get_fk_from_field,
)
from core.myutils import get_current_financial_year

from costcentre.models import CostCentre

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    FinancialYear,
    ForecastMonthlyFigure,
)


def get_month_dict():
    """Link the column names in the ADI file with
    the foreign key used in the MonthlyFigure to
    identify the period"""
    q = FinancialPeriod.objects.filter(
        period_calendar_code__gt=0,
        period_calendar_code__lt=15
    ).values(
        "period_short_name"
    )
    period_dict = {}
    for e in q:
        per_obj, msg = get_fk_from_field(
            FinancialPeriod, "period_short_name", e["period_short_name"]
        )
        period_dict[e["period_short_name"].lower()] = per_obj
    return period_dict


def import_adi_file(csvfile):
    """Read the ADI file and unpivot it to enter the MonthlyFigure data
    Hard coded the year because it is a temporary solution....
    The information is used to create the OSCAR report to be uploaded to Treasury"""
    fin_year = get_current_financial_year()
    # Clear the table first. The adi file has several lines with the same key,
    # so the figures have to be added and we don't want to add to existing data!
    ForecastMonthlyFigure.objects.filter(financial_year=fin_year).delete()
    reader = csv.reader(csvfile)
    col_key = csv_header_to_dict(next(reader))
    line = 1
    fin_obj, msg = get_fk(FinancialYear, fin_year)
    month_dict = get_month_dict()
    csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in csv_reader:
        line += 1
        err_msg = ""
        cc_obj, msg = get_fk(CostCentre, row[col_key["cost centre"]].strip())
        err_msg += msg
        nac_obj, msg = get_fk(NaturalCode, row[col_key["natural account"]].strip())
        err_msg += msg
        prog = row[col_key["programme"]].strip()
        prog_obj, msg = get_fk(ProgrammeCode, prog)
        err_msg += msg
        an1_obj, msg = get_fk(Analysis1, int(row[col_key["analysis"]]))
        an2_obj, msg = get_fk(Analysis2, int(row[col_key["analysis2"]]))
        proj_obj, msg = get_fk(ProjectCode, row[col_key["project"]].strip())
        # Now read the twelve month values into a dict
        if err_msg == "":
            financial_code, created = FinancialCode.objects.get_or_create(
                programme=prog_obj,
                cost_centre=cc_obj,
                natural_account_code=nac_obj,
                analysis1_code=an1_obj,
                analysis2_code=an2_obj,
                project_code=proj_obj,
            )
            if created:
                financial_code.save()

            for month, per_obj in month_dict.items():
                period_amount = int(row[col_key[month.lower()]])
                if period_amount:
                    month_figure_obj, created = \
                        ForecastMonthlyFigure.objects.get_or_create(
                            financial_year=fin_obj,
                            financial_period=per_obj,
                            financial_code=financial_code,
                        )
                    if created:
                        month_figure_obj.amount = period_amount * 100
                    else:
                        month_figure_obj.amount += (period_amount * 100)
                    month_figure_obj.current_amount = month_figure_obj.amount
                    month_figure_obj.save()
        else:
            print(line, err_msg)

        if (line % 100) == 0:
            print(line)


h_list = [
    "cost centre",
    "natural account",
    "programme",
    "analysis",
    "analysis2",
    "project",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan",
    "Feb",
    "Mar",
]

import_adi_file_class = ImportInfo(
    {},
    "DIT Information",
    h_list,
    import_adi_file,
)
