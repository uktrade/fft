from django.db import connection
from django.db.models import Sum

from core.utils.generic_helpers import get_current_financial_year
from forecast.models import ForecastMonthlyFigure
from forecast.utils.query_fields import ForecastQueryFields
from upload_split_file.models import PaySplitCoefficient, TemporaryCalculatedValues


class TransferTooLargeError(Exception):
    pass


PAY_CODE = "Staff UK (Pay)"
INCOME_PAY_CODE = "Income (Pay)"

EXPENDITURE_TYPE_LIST = [PAY_CODE, INCOME_PAY_CODE]


def calculate_expenditure_type_total(
    directorate_code, financial_period_id, expenditure_type_code_list
):
    query_fields = ForecastQueryFields()

    expenditure_type_field = query_fields.budget_category_name_field
    directorate_field = query_fields.directorate_code_field
    pay_total = 0
    for expenditure_type_code in expenditure_type_code_list:
        kwargs = {
            "financial_period_id": financial_period_id,
            "financial_year_id": get_current_financial_year(),
            expenditure_type_field: expenditure_type_code,
            directorate_field: directorate_code,
            "archived_status__isnull": True,
        }
        pay_total_obj = ForecastMonthlyFigure.objects.filter(**kwargs).aggregate(
            Sum("amount")
        )
        if pay_total_obj["amount__sum"]:
            pay_total += pay_total_obj["amount__sum"]
    return pay_total


def copy_values(period_id, directorate_code, expenditure_code_list):
    financial_year_id = get_current_financial_year()
    sql_list = ""
    for expenditure_code in expenditure_code_list:
        sql_list = f"{sql_list} '{expenditure_code}', "

    # clear the previously calculated values
    sql_delete = (
        f"DELETE from public.upload_split_file_splitpayactualfigure "
        f"WHERE financial_period_id = {period_id}"
    )

    # copy the relevant values from main table,
    # setting them to 0
    sql_reset_amount = (
        f"INSERT INTO public.upload_split_file_splitpayactualfigure"
        f"(created, updated, amount, financial_code_id, "
        f"financial_period_id, financial_year_id) "
        f"SELECT now(), now(), 0, financial_code_id, "
        f"financial_period_id, financial_year_id "
        f"FROM forecast_forecastmonthlyfigure AS fm "
        f"INNER JOIN forecast_financialcode fc ON (fm.financial_code_id= fc.id) "
        f"INNER JOIN costcentre_costcentre  ON "
        f"(fc.cost_centre_id = costcentre_costcentre.cost_centre_code) "
        f'INNER JOIN  "chartofaccountDIT_naturalcode" nac '
        f"ON (fc.natural_account_code_id = nac.natural_account_code) "
        f'INNER JOIN "chartofaccountDIT_expenditurecategory" ec '
        f"ON (nac.expenditure_category_id = ec.id) "
        f"WHERE fm.financial_period_id = {period_id} "
        f"AND fm.financial_year_id = {financial_year_id} "
        f"AND fm.archived_status_id is null "
        f"AND costcentre_costcentre.directorate_id = '{directorate_code}' "
        f"AND ec.grouping_description in ( {sql_list} '');"
    )

    sql_update = (
        f"UPDATE upload_split_file_splitpayactualfigure "
        f"SET amount = c.calculated_amount "
        f"FROM upload_split_file_temporarycalculatedvalues c "
        f"WHERE upload_split_file_splitpayactualfigure.financial_period_id "
        f"= {period_id} "
        f"AND upload_split_file_splitpayactualfigure.financial_year_id "
        f"= {financial_year_id} "
        f"AND upload_split_file_splitpayactualfigure.financial_code_id "
        f"= c.financial_code_id;"
    )

    sql_insert = (
        f"INSERT INTO upload_split_file_splitpayactualfigure "
        f"(created, "
        f"updated, amount, "
        f"financial_code_id,  "
        f"financial_period_id, financial_year_id) "
        f"SELECT now(), now(),  calculated_amount, "
        f"financial_code_id, "
        f"{period_id}, {financial_year_id} "
        f"FROM upload_split_file_temporarycalculatedvalues "
        f"WHERE "
        f" financial_code_id "
        f"not in (select financial_code_id "
        f"from upload_split_file_splitpayactualfigure where "
        f"financial_period_id = {period_id} and "
        f"financial_year_id = {financial_year_id});"
    )

    with connection.cursor() as cursor:
        cursor.execute(sql_delete)
        cursor.execute(sql_reset_amount)
        cursor.execute(sql_update)
        cursor.execute(sql_insert)


def handle_split_project_by_directorate(
    financial_period_id, directorate_code, expenditure_code_list
):
    total_value = calculate_expenditure_type_total(
        directorate_code, financial_period_id, expenditure_code_list
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
        transferred_to_obj.save()

    copy_values(financial_period_id, directorate_code, expenditure_code_list)


def handle_split_project(financial_period_id):
    coefficient_queryset = (
        PaySplitCoefficient.objects.filter(financial_period_id=financial_period_id)
        .order_by("directorate_code")
        .distinct("directorate_code")
    )
    for coefficient in coefficient_queryset:
        directorate_code = coefficient.directorate_code
        handle_split_project_by_directorate(
            financial_period_id, directorate_code, EXPENDITURE_TYPE_LIST
        )
