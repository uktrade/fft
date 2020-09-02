import csv
import logging
from decimal import Decimal

from core.import_csv import (
    ImportInfo,
    csv_header_to_dict,
    get_fk,
    get_fk_from_field,
)
from core.utils.generic_helpers import get_current_financial_year

from forecast.models import (
    FinancialPeriod,
    FinancialYear,
    ForecastMonthlyFigure,
)
from forecast.utils.import_helpers import CheckFinancialCode


logger = logging.getLogger(__name__)


class WrongChartOFAccountCodeException(Exception):
    pass


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
    """Read the ADI file and unpivot it to enter the MonthlyFigure data"""
    fin_year = get_current_financial_year()
    # Clear the table first. The adi file has several lines with the same key,
    # so the figures have to be added and we don't want to add to existing data!
    ForecastMonthlyFigure.objects.filter(
        financial_year=fin_year,
        archived_status__isnull=True
    ).delete()
    reader = csv.reader(csvfile)
    col_key = csv_header_to_dict(next(reader))
    line = 1
    fin_obj, msg = get_fk(FinancialYear, fin_year)
    month_dict = get_month_dict()
    check_financial_code = CheckFinancialCode(None)

    csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in csv_reader:
        line += 1
        programme_code = row[col_key["programme"]].strip()
        cost_centre = row[col_key["cost centre"]].strip()
        nac = row[col_key["natural account"]].strip()
        analysis1 = row[col_key["analysis"]].strip()
        analysis2 = row[col_key["analysis2"]].strip()
        project_code = row[col_key["project"]].strip()
        check_financial_code.validate(
            cost_centre, nac, programme_code, analysis1, analysis2, project_code, line
        )

        if check_financial_code.error_found:
            raise WrongChartOFAccountCodeException(
                f"Importing Forecast, Row {line} error: "
                f"{check_financial_code.display_error}"
            )

        financialcode_obj = check_financial_code.get_financial_code()

        for month, per_obj in month_dict.items():
            period_amount = Decimal(row[col_key[month.lower()]])
            if period_amount:
                month_figure_obj, created = \
                    ForecastMonthlyFigure.objects.get_or_create(
                        financial_year=fin_obj,
                        financial_period=per_obj,
                        financial_code=financialcode_obj,
                        archived_status__isnull=True,
                    )
                if created:
                    month_figure_obj.amount = period_amount * 100
                else:
                    month_figure_obj.amount += (period_amount * 100)
                month_figure_obj.current_amount = month_figure_obj.amount
                month_figure_obj.save()

        if (line % 100) == 0:
            logger.info(line)
    return True, "Import completed successfully."


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
