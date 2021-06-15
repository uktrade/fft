from django.db import connection
from django.db.models import Sum

from core.utils.generic_helpers import get_current_financial_year

from forecast.models import ForecastMonthlyFigure
from forecast.utils.query_fields import ForecastQueryFields

from split_project.models import PaySplitCoefficient, TemporaryCalculatedValues


class TransferTooLargeError(Exception):
    pass


PAY_CODE = "Staff UK (Pay)"


def calculate_expenditure_type_total(
    directorate_code, financial_period_id, expenditure_type_code, current_year=True
):
    if current_year:
        query_fields = ForecastQueryFields()
    else:
        previous_year = get_current_financial_year() - 1
        query_fields = ForecastQueryFields(previous_year)

    expenditure_type_field = query_fields.budget_category_name_field
    directorate_field = query_fields.directorate_code_field

    kwargs = {
        "financial_period_id": financial_period_id,
        expenditure_type_field: expenditure_type_code,
        directorate_field: directorate_code,
        "archived_status__isnull": True,
    }

    pay_total = ForecastMonthlyFigure.objects.filter(**kwargs).aggregate(Sum("amount"))
    return pay_total["amount__sum"]


def copy_values(period_id, directorate_code, expenditure_code):
    financial_year_id = get_current_financial_year()
    # clear the previously calculated values
    sql_reset_amount = (
        f"UPDATE forecast_forecastmonthlyfigure  "
        f"SET amount=0 WHERE forecast_forecastmonthlyfigure.ID IN ("
        f"SELECT fm.ID  "
        f"FROM forecast_forecastmonthlyfigure AS fm "
        f"INNER JOIN forecast_financialcode fc ON (fm.financial_code_id= fc.id) "
        f"INNER JOIN costcentre_costcentre  ON "
        f"(fc.cost_centre_id = costcentre_costcentre.cost_centre_code) "
        f'INNER JOIN  "chartofaccountDIT_naturalcode" nac '
        f"ON (fc.natural_account_code_id = nac.natural_account_code) "
        f'INNER JOIN "chartofaccountDIT_expenditurecategory" ec '
        f"ON (nac.expenditure_category_id = ec.id) "
        f"WHERE fm.financial_period_id = {period_id} "
        f"AND fm.archived_status_id is null "
        f"AND costcentre_costcentre.directorate_id = '{directorate_code}' "
        f"AND ec.grouping_description = '{expenditure_code}' );"
    )

    sql_update = (
        f"UPDATE forecast_forecastmonthlyfigure "
        f"SET amount = c.calculated_amount "
        f"FROM split_project_temporarycalculatedvalues c "
        f"WHERE forecast_forecastmonthlyfigure.financial_period_id = {period_id} "
        f"AND forecast_forecastmonthlyfigure.financial_code_id = c.financial_code_id "
        f"AND archived_status_id is null;"
    )

    sql_insert = (
        f"INSERT INTO forecast_forecastmonthlyfigure "
        f"(created, "
        f"updated, amount, oracle_amount, "
        f"financial_code_id,  "
        f"financial_period_id, financial_year_id) "
        f"SELECT now(), now(),  calculated_amount, 0, "
        f"financial_code_id, "
        f"{period_id}, {financial_year_id} "
        f"FROM split_project_temporarycalculatedvalues "
        f"WHERE "
        f" financial_code_id "
        f"not in (select financial_code_id "
        f"from forecast_forecastmonthlyfigure where "
        f"financial_period_id = {period_id} and "
        f"financial_year_id = {financial_year_id});"
    )

    with connection.cursor() as cursor:
        cursor.execute(sql_reset_amount)
        cursor.execute(sql_update)
        cursor.execute(sql_insert)


def handle_split_project_by_directorate(
    financial_period_id, directorate_code, expenditure_code
):
    # for the moment, limit to DDaT
    total_value = calculate_expenditure_type_total(
        directorate_code, financial_period_id, expenditure_code
    )

    # Clear the table used to stored the results while doing the calculations
    TemporaryCalculatedValues.objects.all().delete()

    # Order by split_coefficient, so the last item is the largest coefficient
    # The possible rounding error is added to this row: as it is the largest value,
    # it will be the one least affected by adding the rounding value
    # Doing it like this, ensure that the total of pay is identical before and
    # after splitting
    coefficient_queryset = PaySplitCoefficient.objects.filter(
        financial_period_id=financial_period_id, directorate_code=directorate_code
    ).order_by("split_coefficient")

    transferred_value = 0
    for coefficient in coefficient_queryset:
        value_to_transfer = round((total_value * coefficient.split_coefficient) / 10000)
        transferred_value += value_to_transfer
        if transferred_value > (total_value * 1.01):
            # This error should never happen, because the percentages are checked
            # when uploading the data file.

            raise TransferTooLargeError("Pay split percentage higher that 100%.")
            return
        transferred_to_obj, created = TemporaryCalculatedValues.objects.get_or_create(
            financial_code_id=coefficient.financial_code_to_id,
            calculated_amount=value_to_transfer,
        )
        if created:
            transferred_to_obj.calculated_amount = value_to_transfer
        else:
            transferred_to_obj.calculated_amount += value_to_transfer
        transferred_to_obj.save()

    # Check the rounding
    rounding = total_value - transferred_value
    if rounding:
        # allocate to the last processed row the difference
        transferred_to_obj.calculated_amount += rounding
        transferred_to_obj.save

    copy_values(financial_period_id, directorate_code, expenditure_code)


def handle_split_project(financial_period_id):
    coefficient_queryset = (
        PaySplitCoefficient.objects.filter(financial_period_id=financial_period_id)
        .order_by("directorate_code")
        .distinct("directorate_code")
    )
    for coefficient in coefficient_queryset:
        directorate_code = coefficient.directorate_code
        handle_split_project_by_directorate(
            financial_period_id, directorate_code, PAY_CODE
        )
