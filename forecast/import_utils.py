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


class UploadFileFormatError(Exception):
    pass


class UploadFileDataError(Exception):
    pass


def get_project_obj(code):
    project_code = get_id(code, 4)
    if project_code:
        obj, message = get_fk(ProjectCode, project_code)
    else:
        obj = None
        message = ""
    return obj, message


def get_analysys1_obj(code):
    analysis1_code = get_id(code, 6)
    if analysis1_code:
        obj, message = get_fk(Analysis1, analysis1_code)
    else:
        obj = None
        message = ""
    return obj, message


def get_analysys2_obj(code):
    analysis2_code = get_id(code, 6)
    if analysis2_code:
        obj, message = get_fk(Analysis2, analysis2_code)
    else:
        obj = None
        message = ""
    return obj, message


def sql_for_data_copy(data_type):
    if data_type == FileUpload.ACTUALS:
        temp_data_file = 'forecast_uploadingactuals'
        target = 'forecast_monthlyfigure'
        what = 'amount'
    else:
        if data_type == FileUpload.BUDGET:
            temp_data_file = 'forecast_uploadingbudgets'
            target = 'forecast_budget'
            what = 'budget'
        else:
            raise UploadFileDataError(
                'Unknown upload type.'
            )

    return 'INSERT INTO {}(' \
           'created, ' \
           'updated, ' \
           'active,  ' \
           'analysis1_code_id, ' \
           'analysis2_code_id, ' \
           'cost_centre_id, ' \
           'financial_period_id, ' \
           'financial_year_id, ' \
           'natural_account_code_id, ' \
           'programme_id, ' \
           'project_code_id, ' \
           '{}, ' \
           'forecast_expenditure_type_id)' \
           ' SELECT  ' \
           'now(), ' \
           'now(), ' \
           'active,  ' \
           'analysis1_code_id, ' \
           'analysis2_code_id, ' \
           'cost_centre_id, ' \
           'financial_period_id, ' \
           'financial_year_id, ' \
           'natural_account_code_id, ' \
           'programme_id, ' \
           'project_code_id, ' \
           'amount, ' \
           'forecast_expenditure_type_id ' \
           ' FROM {};'.format(target, what, temp_data_file)


def validate_excel_file(file_upload, ws_title):
    try:
        wb = load_workbook(
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

    ws = wb.worksheets[0]
    if ws.title != ws_title:
        # wrong file
        raise UploadFileFormatError(
            "File appears to be incorrect: worksheet name is '{}', "
            "expected name is '{}".format(ws.title, ws_title)
        )
    return wb, ws


def get_id(value, length=0):
    if value:
        if length:
            a = f"{value}"
            return a.zfill(length)
        else:
            return value
    return None


def get_forecast_month_dict():
    """Link the column names in the ADI file with
    the foreign key used in the MonthlyFigure to
    identify the period"""
    q = FinancialPeriod.objects. \
        filter(period_calendar_code__gt=0,
               period_calendar_code__lt=15,
               actual_loaded=False).values("period_short_name")
    period_dict = {}
    for e in q:
        per_obj, msg = get_fk_from_field(
            FinancialPeriod, "period_short_name", e["period_short_name"]
        )
        period_dict[e["period_short_name"].lower()] = per_obj
    return period_dict
