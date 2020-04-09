from django.db import connection

from chartofaccountDIT.models import (
    NaturalCode,
    ProgrammeCode,
)

from core.import_csv import get_fk, xslx_header_to_dict
from core.models import FinancialYear

from costcentre.models import CostCentre

from forecast.import_utils import (
    UploadFileDataError,
    UploadFileFormatError,
    get_analysys1_obj,
    get_analysys2_obj,
    get_error_from_list,
    get_forecast_month_dict,
    get_project_obj,
    sql_for_data_copy,
    validate_excel_file,
)
from forecast.models import (
    BudgetMonthlyFigure,
    BudgetUploadMonthlyFigure,
    FinancialCode,
)

from upload_file.models import FileUpload
from upload_file.utils import set_file_upload_error

EXPECTED_BUDGET_HEADERS = [
    'cost centre',
    'natural account',
    'programme',
    'analysis',
    'analysis2',
    'project',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec',
    'jan',
    'feb',
    'mar',
]


def check_budget_header(header_dict, correct_header):
    error_msg = ''
    correct = True
    for elem in correct_header:
        if elem not in header_dict:
            correct = False
            error_msg += f"'{elem}' not found. "
    if not correct:
        raise UploadFileFormatError(f'Error in the header: {error_msg}')


def copy_uploaded_budget(year, month_dict):
    for m, period_obj in month_dict.items():
        # Now copy the newly uploaded budgets to the monthly figure table
        BudgetMonthlyFigure.objects.filter(
            financial_year=year,
            financial_period=period_obj,
        ).update(amount=0, starting_amount=0)
        sql_update, sql_insert = \
            sql_for_data_copy(FileUpload.BUDGET, period_obj.pk, year)
        with connection.cursor() as cursor:
            cursor.execute(sql_insert)
            cursor.execute(sql_update)
        BudgetMonthlyFigure.objects.filter(
            financial_year=year,
            financial_period=period_obj,
            amount=0,
            starting_amount=0
        ).delete()
        BudgetUploadMonthlyFigure.objects.filter(
            financial_year=year,
            financial_period=period_obj
        ).delete()


def get_primary_nac_obj(code):
    nac_obj, message = get_fk(NaturalCode, code)
    if nac_obj:
        #  Error if NAC is not a primary nac
        if not nac_obj.used_for_budget:
            message = f'{code}-{nac_obj.natural_account_code_description} ' \
                      f'is not a Primary NAC. \n'
    else:
        nac_obj = None
        message = ""
    return nac_obj, message


def upload_budget(worksheet, year, header_dict):
    year_obj, created = FinancialYear.objects.get_or_create(financial_year=year)
    if created:
        year_obj.financial_year_display = f'{year}/{year - 1999}'
        year_obj.save()

    month_dict = get_forecast_month_dict()
    # Clear the table used to upload the budgets.
    # The budgets are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    BudgetUploadMonthlyFigure.objects.filter(
        financial_year=year,
    ).delete()

    for row in range(2, worksheet.max_row + 1):
        cost_centre = worksheet[f"{header_dict['cost centre']}{row}"].value
        if not cost_centre:
            break
        nac = worksheet[f"{header_dict['natural account']}{row}"].value
        programme_code = worksheet[f"{header_dict['programme']}{row}"].value
        analysis1 = worksheet[f"{header_dict['analysis']}{row}"].value
        analysis2 = worksheet[f"{header_dict['analysis2']}{row}"].value
        project_code = worksheet[f"{header_dict['project']}{row}"].value
        error_list = []
        nac_obj, message = get_primary_nac_obj(nac)
        error_list.append(message)
        cc_obj, message = get_fk(CostCentre, cost_centre)
        error_list.append(message)
        programme_obj, message = get_fk(ProgrammeCode, programme_code)
        error_list.append(message)
        analysis1_obj, message = get_analysys1_obj(analysis1)
        error_list.append(message)
        analysis2_obj, message = get_analysys2_obj(analysis2)
        error_list.append(message)
        project_obj, message = get_project_obj(project_code)
        error_list.append(message)
        error_message = get_error_from_list(error_list)
        if error_message:
            raise UploadFileDataError(
                f'Row {row}: {error_message} not valid.'
            )

        for month, period_obj in month_dict.items():
            period_budget = worksheet[f"{header_dict[month.lower()]}{row}"].value
            if period_budget:
                financialcode_obj, created = FinancialCode.objects.get_or_create(
                    programme=programme_obj,
                    cost_centre=cc_obj,
                    natural_account_code=nac_obj,
                    analysis1_code=analysis1_obj,
                    analysis2_code=analysis2_obj,
                    project_code=project_obj,
                )
                financialcode_obj.save()

                budget_obj, created = BudgetUploadMonthlyFigure.objects.get_or_create(
                    financial_year=year_obj,
                    financial_code=financialcode_obj,
                    financial_period=period_obj,
                )

                if created:
                    # to avoid problems with precision,
                    # we store the figures in pence
                    budget_obj.amount = period_budget * 100
                else:
                    budget_obj.amount += period_budget * 100
                budget_obj.save()

    copy_uploaded_budget(year, month_dict)


def upload_budget_from_file(file_upload, year):
    try:
        workbook, worksheet = validate_excel_file(file_upload, "Budgets")
    except UploadFileFormatError as ex:
        set_file_upload_error(
            file_upload,
            str(ex),
            str(ex),
        )
        raise ex
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_budget_header(header_dict, EXPECTED_BUDGET_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_error(
            file_upload,
            str(ex),
            str(ex),
        )
        workbook.close
        raise ex
    try:
        upload_budget(worksheet, year, header_dict)
    except (UploadFileDataError) as ex:
        set_file_upload_error(
            file_upload,
            str(ex),
            str(ex),
        )
        workbook.close
        raise ex
    workbook.close
    return True
