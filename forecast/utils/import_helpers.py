from zipfile import BadZipFile

from openpyxl import load_workbook

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)

from core.import_csv import (
    get_fk,
    get_fk_from_field,
    get_pk_verbose_name,
)

from costcentre.models import CostCentre

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_error,
    set_file_upload_fatal_error,
    set_file_upload_warning,
)


# When the following codes are used, they must be a fixed length and padded with "0"
ANALYSIS1_CODE_LENGTH = 5
ANALYSIS2_CODE_LENGTH = 5
PROJECT_CODE_LENGTH = 4


def sql_for_data_copy(data_type, financial_period_id, financial_year_id):
    if data_type == FileUpload.ACTUALS:
        temp_data_file = "forecast_actualuploadmonthlyfigure"
        target = "forecast_forecastmonthlyfigure"
    else:
        if data_type == FileUpload.BUDGET:
            temp_data_file = "forecast_budgetuploadmonthlyfigure"
            target = "forecast_budgetmonthlyfigure"
        else:
            raise UploadFileDataError("Unknown upload type.")

    sql_update = (
        f"UPDATE {target} t "
        f"SET  updated=now(), amount=u.amount, starting_amount=u.amount	"
        f"FROM {temp_data_file} u "
        f"WHERE  "
        f"t.financial_code_id = u.financial_code_id and "
        f"t.financial_period_id = u.financial_period_id and "
        f"t.financial_year_id = u.financial_year_id and "
        f"t.financial_period_id = {financial_period_id} and "
        f"t.financial_year_id = {financial_year_id};"
    )

    sql_insert = (
        f"INSERT INTO {target}(created, "
        f"updated, amount, starting_amount, financial_code_id, "
        f"financial_period_id, financial_year_id) "
        f"SELECT now(), now(), amount, amount, financial_code_id, "
        f"financial_period_id, financial_year_id "
        f"FROM {temp_data_file} "
        f"WHERE "
        f"financial_period_id = {financial_period_id} and "
        f"financial_year_id = {financial_year_id}  and "
        f" financial_code_id "
        f"not in (select financial_code_id "
        f"from {target} where "
        f"financial_period_id = {financial_period_id} and "
        f"financial_year_id = {financial_year_id});"
    )

    return sql_update, sql_insert


class UploadFileFormatError(Exception):
    pass


class UploadFileDataError(Exception):
    pass


def validate_excel_file(file_upload, worksheet_title_pattern):
    try:
        # read_only=True makes the opening process much faster
        # data_only=True to read values from cells with formula.
        # otherwise the formula is returned instead of the value.
        workbook = load_workbook(
            file_upload.document_file, read_only=True, data_only=True,
        )
    except BadZipFile as ex:
        set_file_upload_fatal_error(
            file_upload,
            "The file is not in the correct format (.xlsx)",
            "BadZipFile (user file is not .xlsx)",
        )
        raise ex
    worksheet_found = False
    worksheet = None
    for ws in workbook:
        if ws.title[: len(worksheet_title_pattern)] == worksheet_title_pattern:
            worksheet_found = True
            worksheet = ws
            break

    if worksheet_found:
        return workbook, worksheet
    # wrong file
    raise UploadFileFormatError(
        f"File appears to be incorrect:  "
        f"it does not contain a worksheet "
        f"with name starting by {worksheet_title_pattern}"
    )


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
        financial_period_code__gt=actual_month, financial_period_code__lt=13
    ).values("period_short_name")
    period_dict = {}
    for e in q:
        per_obj, msg = get_fk_from_field(
            FinancialPeriod, "period_short_name", e["period_short_name"]
        )
        period_dict[e["period_short_name"].lower()] = per_obj

    return period_dict


def get_error_from_list(error_list):
    error_message = ""
    for item in error_list:
        if item and item != "":
            error_message = f"{error_message}, {item}"
    if error_message != "":
        error_message = error_message[:-1]
    return error_message


def get_primary_nac_obj(code):
    nac_obj, message = get_fk(NaturalCode, code)
    if nac_obj:
        #  Error if NAC is not a primary nac
        if not nac_obj.used_for_budget:
            message = (
                f"{code}-{nac_obj.natural_account_code_description} "
                f"is not a Primary NAC. \n"
            )
    else:
        nac_obj = None
        message = ""
    return nac_obj, message


CODE_OK = 1
CODE_ERROR = 2
CODE_WARNING = 3
IGNORE = 4

obj_index = 0
status_index = 1
message_index = 2

VALID_ECONOMIC_CODE_LIST = ["RESOURCE", "CAPITAL"]


class CheckFinancialCode:
    display_error = ""
    display_warning = ""
    financial_code_obj = None
    error_found = False
    warning_found = False
    ignore_row = False
    # Dictionary of tuples
    # Each tuple contains : (obj, status, error_code, message)
    # The objects of codes already used are kept in the dictionary,
    # to reduce the number of database accesses
    nac_dict = {}
    cc_dict = {}
    prog_dict = {}
    analysis1_dict = {}
    analysis2_dict = {}
    project_dict = {}

    error_row = 0

    def get_info_tuple(self, model, pk):
        obj, msg = get_fk(model, pk)
        if not obj:
            status = CODE_ERROR
        else:
            if not obj.active:
                if self.upload_type == FileUpload.BUDGET:
                    status = CODE_ERROR
                    msg = (
                        f'{get_pk_verbose_name(model)} "{pk}" '
                        f"is not in the approved list. \n"
                    )
                    obj = None
                else:
                    obj.active
                    obj.save
                    status = CODE_WARNING
                    msg = (
                        f'{get_pk_verbose_name(model)} "{pk}" '
                        f"added to the approved list. \n"
                    )
            else:
                status = CODE_OK
                msg = ""
        info_tuple = (obj, status, msg)
        return info_tuple

    def __init__(self, file_upload):
        self.file_upload = file_upload
        self.upload_type = self.file_upload.document_type
        self.error_found = False
        self.warning_found = False
        self.nac_dict = {}
        self.cc_dict = {}
        self.prog_dict = {}
        self.analysis1_dict = {}
        self.analysis2_dict = {}
        self.project_dict = {}

    def validate_info_tuple(self, info_tuple):
        status = info_tuple[status_index]
        msg = info_tuple[message_index]
        obj = info_tuple[obj_index]

        if status == CODE_ERROR:
            self.error_found = True
            self.display_error = self.display_error + msg
        else:
            if status == CODE_WARNING:
                self.warning_found = True
                self.display_warning = self.display_warning + msg
        return obj

    def get_obj_code(self, code_dict, code, model_name):
        # protection in case the code was read from an empty cell
        if code is None:
            code = 0
        info_tuple = code_dict.get(code, None)
        if not info_tuple:
            info_tuple = self.get_info_tuple(model_name, code)
            code_dict[code] = info_tuple
        return self.validate_info_tuple(info_tuple)

    def validate_nac_for_budget(self, nac):
        if nac is None:
            nac = 0
        info_tuple = self.nac_dict.get(nac, None)
        if not info_tuple:
            info_tuple = self.get_info_tuple(NaturalCode, nac)
            if info_tuple[status_index] == CODE_OK:
                obj = info_tuple[obj_index]
                #  test if the nac is a primary nac
                if not obj.used_for_budget:
                    status = CODE_WARNING
                    msg = f'Natural Account "{nac}" is not a primary NAC.\n'
                    info_tuple = (obj, status, msg)

            self.nac_dict[nac] = info_tuple
        return self.validate_info_tuple(info_tuple)

    def validate_nac_for_actual(self, nac):
        info_tuple = self.nac_dict.get(nac, None)
        if not info_tuple:
            info_tuple = self.get_info_tuple(NaturalCode, nac)
            if info_tuple[status_index] != CODE_ERROR:
                obj = info_tuple[obj_index]
                #  Check that the NAC is resource or capital
                # If not, we skip the row
                if (
                    not obj.economic_budget_code
                    or obj.economic_budget_code.upper() not in VALID_ECONOMIC_CODE_LIST
                ):
                    status = IGNORE
                    msg = ""
                    info_tuple = (None, status, msg)

            self.nac_dict[nac] = info_tuple
        if info_tuple[status_index] == IGNORE:
            self.ignore_row = True
        return self.validate_info_tuple(info_tuple)

    def validate_cost_centre(self, cost_centre):
        return self.get_obj_code(self.cc_dict, cost_centre, CostCentre)

    def validate_programme(self, programme_code):
        return self.get_obj_code(self.prog_dict, programme_code, ProgrammeCode)

    def validate_analysis1(self, analysis1):
        if analysis1 and int(analysis1):
            analysis1_code = get_id(analysis1, ANALYSIS1_CODE_LENGTH)
            return self.get_obj_code(self.analysis1_dict, analysis1_code, Analysis1)
        else:
            return None

    def validate_analysis2(self, analysis2):
        if analysis2 and int(analysis2):
            analysis2_code = get_id(analysis2, ANALYSIS1_CODE_LENGTH)
            return self.get_obj_code(self.analysis2_dict, analysis2_code, Analysis2)
        else:
            return None

    def validate_project(self, project):
        if project and int(project):
            project_code = get_id(project, PROJECT_CODE_LENGTH)
            return self.get_obj_code(self.project_dict, project_code, ProjectCode)
        else:
            return None

    def validate(
        self, cost_centre, nac, programme, analysis1, analysis2, project, row_number
    ):
        self.display_error = ""
        self.display_warning = ""
        self.ignore_row = False
        if self.upload_type == FileUpload.BUDGET:
            self.nac_obj = self.validate_nac_for_budget(nac)
        else:
            self.nac_obj = self.validate_nac_for_actual(nac)
            if self.ignore_row:
                return
        self.programme_obj = self.validate_programme(programme)
        self.cc_obj = self.validate_cost_centre(cost_centre)
        self.analysis1_obj = self.validate_analysis1(analysis1)
        self.analysis2_obj = self.validate_analysis2(analysis2)
        self.project_obj = self.validate_project(project)

        if self.display_warning:
            set_file_upload_warning(
                self.file_upload, f"Row {row_number} warning: {self.display_warning}"
            )

        if self.display_error:
            set_file_upload_error(
                self.file_upload,
                f"Row {row_number} error: {self.display_error}",
                "Upload aborted: Data error.",
            )
        return self.error_found

    def get_financial_code(self):
        if self.error_found:
            return None
        financial_code_obj, created = FinancialCode.objects.get_or_create(
            programme=self.programme_obj,
            cost_centre=self.cc_obj,
            natural_account_code=self.nac_obj,
            analysis1_code=self.analysis1_obj,
            analysis2_code=self.analysis2_obj,
            project_code=self.project_obj,
        )
        financial_code_obj.save()
        return financial_code_obj
