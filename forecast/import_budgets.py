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
    get_forecast_month_dict,
    get_project_obj,
    sql_for_data_copy,
    validate_excel_file,
)
from forecast.models import (
    Budget,
    UploadingBudgets,
)

from upload_file.models import FileUpload
from upload_file.utils import set_file_upload_error

EXPECTED_BUDGET_HEADERS = ['cost centre',
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
                           'mar']


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
    # Now copy the newly uploaded actuals to the monthly figure table
    for month, period_obj in month_dict.items():
        Budget.objects.filter(
            financial_year=year,
            financial_period=period_obj,
        ).delete()
    with connection.cursor() as cursor:
        cursor.execute(sql_for_data_copy(FileUpload.BUDGET))
    UploadingBudgets.objects.filter(
        financial_year=year,
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


def upload_budget(ws, year, header_dict):
    year_obj, created = FinancialYear.objects.get_or_create(financial_year=year)
    if created:
        year_obj.financial_year_display = f'{year}/{year - 1999}'
        year_obj.save()

    month_dict = get_forecast_month_dict()
    # Clear the table used to upload the budgets.
    # The budgets are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    UploadingBudgets.objects.filter(
        financial_year=year,
    ).delete()
    for row in range(2, ws.max_row + 1):
        cost_centre = ws["{}{}".format(header_dict["cost centre"], row)].value
        if not cost_centre:
            break
        error_message = ''
        nac = ws["{}{}".format(header_dict["natural account"], row)].value
        programme_code = ws["{}{}".format(header_dict["programme"], row)].value
        analisys1 = ws["{}{}".format(header_dict["analysis"], row)].value
        analisys2 = ws["{}{}".format(header_dict["analysis2"], row)].value
        project_code = ws["{}{}".format(header_dict["project"], row)].value

        nac_obj, message = get_primary_nac_obj(nac)
        error_message += message
        cc_obj, message = get_fk(CostCentre, cost_centre)
        error_message += message
        programme_obj, message = get_fk(ProgrammeCode, programme_code)
        error_message += message
        analysis1_obj, message = get_analysys1_obj(analisys1)
        error_message += message
        analysis2_obj, message = get_analysys2_obj(analisys2)
        error_message += message
        project_obj, message = get_project_obj(project_code)
        error_message += message
        if error_message:
            raise UploadFileDataError(
                f'Error at row {row}: {error_message}.'
            )

        for month, period_obj in month_dict.items():
            period_budget = ws["{}{}".format(header_dict[month.lower()], row)].value
            if period_budget:
                budget_obj, created = UploadingBudgets.objects.get_or_create(
                    financial_year=year_obj,
                    programme=programme_obj,
                    cost_centre=cc_obj,
                    natural_account_code=nac_obj,
                    analysis1_code=analysis1_obj,
                    analysis2_code=analysis2_obj,
                    project_code=project_obj,
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
        wb, ws = validate_excel_file(file_upload, "Budgets")
    except UploadFileFormatError as ex:
        set_file_upload_error(
            file_upload,
            str(ex),
            str(ex),
        )
        raise ex
    header_dict = xslx_header_to_dict(ws[1])
    try:
        check_budget_header(header_dict, EXPECTED_BUDGET_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_error(
            file_upload,
            str(ex),
            str(ex),
        )
        wb.close
        raise ex
    try:
        upload_budget(ws, year, header_dict)
    except UploadFileDataError as ex:
        set_file_upload_error(
            file_upload,
            str(ex),
            str(ex),
        )
        wb.close
        raise ex
    wb.close
    return True
