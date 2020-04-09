from zipfile import BadZipFile

from openpyxl import load_workbook

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    ProjectCode,
)

from core.import_csv import get_fk, get_fk_from_field

from forecast.models import (
    FinancialPeriod,
)

from upload_file.models import FileUpload
from upload_file.utils import set_file_upload_error

# When the following codes are used, they must be a fixed length and padded with "0"
ANALYSIS1_CODE_LENGTH = 5
ANALYSIS2_CODE_LENGTH = 5
PROJECT_CODE_LENGTH = 4


def sql_for_data_copy(data_type, financial_period_id, financial_year_id):
    if data_type == FileUpload.ACTUALS:
        temp_data_file = 'forecast_actualuploadmonthlyfigure'
        target = 'forecast_forecastmonthlyfigure'
    else:
        if data_type == FileUpload.BUDGET:
            temp_data_file = 'forecast_budgetuploadmonthlyfigure'
            target = 'forecast_budgetmonthlyfigure'
        else:
            raise UploadFileDataError(
                'Unknown upload type.'
            )

    sql_update = f'UPDATE {target} t ' \
                 f'SET  updated=now(), amount=u.amount, starting_amount=u.amount	' \
                 f'FROM {temp_data_file} u ' \
                 f'WHERE  ' \
                 f't.financial_code_id = u.financial_code_id and ' \
                 f't.financial_period_id = u.financial_period_id and ' \
                 f't.financial_year_id = u.financial_year_id and ' \
                 f't.financial_period_id = {financial_period_id} and ' \
                 f't.financial_year_id = {financial_year_id};'

    sql_insert = f'INSERT INTO {target}(created, ' \
                 f'updated, amount, starting_amount, financial_code_id, ' \
                 f'financial_period_id, financial_year_id) ' \
                 f'SELECT now(), now(), amount, amount, financial_code_id, ' \
                 f'financial_period_id, financial_year_id ' \
                 f'FROM {temp_data_file} ' \
                 f'WHERE ' \
                 f'financial_period_id = {financial_period_id} and ' \
                 f'financial_year_id = {financial_year_id}  and ' \
                 f' financial_code_id ' \
                 f'not in (select financial_code_id ' \
                 f'from {target} where ' \
                 f'financial_period_id = {financial_period_id} and ' \
                 f'financial_year_id = {financial_year_id});'

    return sql_update, sql_insert


class UploadFileFormatError(Exception):
    pass


class UploadFileDataError(Exception):
    pass


def get_project_obj(code):
    if int(code):
        project_code = get_id(code, PROJECT_CODE_LENGTH)
        obj, message = get_fk(ProjectCode, project_code)
    else:
        obj = None
        message = ""
    return obj, message


def get_analysys1_obj(code):
    if int(code):
        analysis1_code = get_id(code, ANALYSIS1_CODE_LENGTH)
        obj, message = get_fk(Analysis1, analysis1_code)
    else:
        obj = None
        message = ""
    return obj, message


def get_analysys2_obj(code):
    if int(code):
        analysis2_code = get_id(code, ANALYSIS2_CODE_LENGTH)
        obj, message = get_fk(Analysis2, analysis2_code)
    else:
        obj = None
        message = ""
    return obj, message


def validate_excel_file(file_upload, worksheet_title):
    try:
        workbook = load_workbook(
            file_upload.document_file,
            read_only=True,
        )
    except BadZipFile as ex:
        set_file_upload_error(
            file_upload,
            "The file is not in the correct format (.xlsx)",
            "BadZipFile (user file is not .xlsx)",
        )
        raise ex

    worksheet = workbook.worksheets[0]
    if worksheet.title != worksheet_title:
        # wrong file
        raise UploadFileFormatError(
            "File appears to be incorrect: worksheet name is '{}', "
            "expected name is '{}".format(worksheet.title, worksheet_title)
        )
    return workbook, worksheet


def get_id(value, length=0):
    if value:
        if length:
            a = f"{value}"
            return a.zfill(length)
        else:
            return value
    return None


def get_forecast_month_dict():
    """Link the column names in the budget file to
    the foreign key used in the budget model to
    identify the period.
    Exclude months were actuals have been uploaded."""
    actual_month = FinancialPeriod.financial_period_info.actual_month()
    q = FinancialPeriod.objects.filter(
        financial_period_code__gt=actual_month,
        financial_period_code__lt=13
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


def get_error_from_list(error_list):
    error_message = ''
    for item in error_list:
        if item and item != '':
            error_message = f'{error_message}, {item}'
    if error_message != '':
        error_message = error_message[:-1]
    return error_message
