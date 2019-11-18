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

from costcentre.models import CostCentre

from forecast.models import FinancialPeriod, FinancialYear, MonthlyFigure


def get_month_dict():
    """Link the column names in the ADI file with
    the foreign key used in the MonthlyFigure to
    identify the period"""
    q = FinancialPeriod.objects.filter(period_calendar_code__gt=0).values(
        "period_short_name"
    )
    my_dict = {}
    for e in q:
        per_obj, msg = get_fk_from_field(
            FinancialPeriod, "period_short_name", e["period_short_name"]
        )
        my_dict[e["period_short_name"].lower()] = per_obj
    return my_dict


def import_adi_file(csvfile):
    """Read the ADI file and unpivot it to enter the MonthlyFigure data
    Hard coded the year because it is a temporary solution....
    The information is used to create the OSCAR report to be uploaded to Treasury"""
    fin_year = 2019
    # Clear the table first. The adi file has several lines with the same key,
    # so the figures have to be added and we don't want to add to existing data!
    MonthlyFigure.objects.filter(financial_year=fin_year).delete()
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
        proj_obj, msg = get_fk(ProjectCode, row[col_key["spare2"]].strip())
        # Now read the twelve month values into a dict
        if err_msg == "":
            for month, per_obj in month_dict.items():
                period_amount = int(row[col_key[month.lower()]])
                adi_obj, created = MonthlyFigure.objects.get_or_create(
                    financial_year=fin_obj,
                    programme=prog_obj,
                    cost_centre=cc_obj,
                    natural_account_code=nac_obj,
                    analysis1_code=an1_obj,
                    analysis2_code=an2_obj,
                    project_code=proj_obj,
                    financial_period=per_obj,
                )
                if created:
                    adi_obj.amount = period_amount
                else:
                    adi_obj.amount += period_amount
                adi_obj.save()
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
    "spare2",
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


def import_unpivot_actual(csv_file, fin_year):
    reader = csv.reader(csv_file)
    col_key = csv_header_to_dict(next(reader))
    print(col_key)
    line = 2
    fin_obj, msg = get_fk(FinancialYear, fin_year)
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
    for row in csv_reader:
        line += 1
        err_msg = ""
        cc_obj, msg = get_fk(CostCentre, row[col_key["cost centre"]].strip())
        err_msg += msg
        nac_obj, msg = get_fk(NaturalCode, row[col_key["natural account"]].strip())
        err_msg += msg
        prog = row[col_key["programme"]].strip()
        if prog == 0:
            prog = 310801
        prog_obj, msg = get_fk(ProgrammeCode, prog)
        err_msg += msg
        per_obj, msg = get_fk_from_field(
            FinancialPeriod, "period_short_name", row[col_key["period"]].strip()
        )
        err_msg += msg

        an1_obj, msg = get_fk(Analysis1, int(row[col_key["analysis"]]))
        an2_obj, msg = get_fk(Analysis2, int(row[col_key["analysis2"]]))
        proj_obj, msg = get_fk(ProjectCode, row[col_key["spare2"]].strip())
        period_amount = int(row[col_key["amount"]])
        if err_msg == "":
            adi_obj, created = MonthlyFigure.objects.get_or_create(
                financial_year=fin_obj,
                programme=prog_obj,
                cost_centre=cc_obj,
                natural_account_code=nac_obj,
                analysis1_code=an1_obj,
                analysis2_code=an2_obj,
                project_code=proj_obj,
                financial_period=per_obj,
            )
            adi_obj.amount = period_amount
            adi_obj.save()
            if not line % 1000:
                print(line)
        else:
            print("Error at line ", line, err_msg)
