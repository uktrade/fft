import datetime

from django.db import connection

from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from core.import_csv import xslx_header_to_dict
from core.models import FinancialYear

from costcentre.models import ArchivedCostCentre

from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileDataError,
    UploadFileFormatError,
    check_header,
    validate_excel_file,
)

from previous_years.models import (
    ArchivedFinancialCode,
    ArchivedForecastData,
    ArchivedForecastDataUpload,
)
from previous_years.utils import (
    ArchiveYearError,
    validate_year_for_archiving_actuals,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

# Make the adjustment columns compulsory. They can have just 0 in it.
# Maybe only one adjustment column is needed, but it becomes too complex to find out
# if it is required or not. This process will only happen 3 or 4 times a year,
# so it is not a big deal to add the required columns to the Excel file
DATA_HEADERS = [
    "budget",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
    "jan",
    "feb",
    "mar",
    "adj01",
    "adj02",
    "adj03",
]

COST_CENTRE_HEADER = "cost centre"
NAC_HEADER = "natural account"
PROGRAMME_HEADER = "programme"
PROJECT_HEADER = "project"
ANALYSIS_HEADER = "analysis"
ANALYSIS2_HEADER = "analysis2"

VALID_WS_NAME = "Outturn"


class CheckArchivedFinancialCode(CheckFinancialCode):
    """Uses the logic in CheckFinancialCode, but extract
    the chart of account from the archived tables"""

    def __init__(self, financial_year, file_upload):
        self.cost_centre_model = ArchivedCostCentre
        self.programme_code_model = ArchivedProgrammeCode
        self.analysis1_model = ArchivedAnalysis1
        self.analysis2_model = ArchivedAnalysis2
        self.project_code_model = ArchivedProjectCode
        self.natural_code_model = ArchivedNaturalCode
        self.financial_year = financial_year
        super().__init__(file_upload)

    def get_chart_of_account_object(self, m, value):
        msg = ""
        try:
            field_name = m.chart_of_account_code_name
            kwargs = {}
            kwargs[field_name] = value
            kwargs["financial_year_id"] = self.financial_year
            obj = m.objects.get(**kwargs)
        except m.DoesNotExist:
            msg = f'{field_name} "{value}" does not exist.\n'
            obj = None
        except ValueError:
            msg = f'{field_name} "{value}" is the wrong type.\n'
            obj = None
        return obj, msg

    def get_info_tuple(self, model, pk, make_active=True):
        status = self.IGNORE
        obj, msg = self.get_chart_of_account_object(model, pk)
        if not obj:
            status = self.CODE_ERROR
        else:
            if obj.active:
                status = self.CODE_OK
                msg = ""
            else:
                if make_active:
                    obj.active = True
                    obj.save()
                    status = self.CODE_WARNING
                    msg = (
                        f'{(model.chart_of_account_code_name)} "{pk}" '
                        f"added to the approved list. \n"
                    )
        info_tuple = (obj, status, msg)
        return info_tuple

    def get_financial_code(self):
        if self.error_found:
            return None
        financial_code_obj, created = ArchivedFinancialCode.objects.get_or_create(
            programme=self.programme_obj,
            cost_centre=self.cc_obj,
            natural_account_code=self.nac_obj,
            analysis1_code=self.analysis1_obj,
            analysis2_code=self.analysis2_obj,
            project_code=self.project_obj,
            financial_year_id=self.financial_year,
        )
        financial_code_obj.save()
        return financial_code_obj


def copy_uploaded_previous_year(year):
    # Now copy the newly uploaded previous_years to the monthly figure table
    ArchivedForecastData.objects.filter(financial_year=year,).delete()
    sql_insert = (
        "INSERT INTO previous_years_archivedforecastdata("
        "created, "
        "updated, "
        "archived, "
        "budget, "
        "apr, "
        "may, "
        "jun, "
        "jul, "
        "aug, "
        "sep, "
        "oct, "
        "nov, "
        '"dec", '
        "jan, "
        "feb, "
        "mar, "
        "adj1, "
        "adj2, "
        "adj3, "
        "financial_code_id, "
        "financial_year_id) "
        "SELECT "
        "created, "
        "updated, "
        "archived, "
        "budget, "
        "apr, "
        "may, "
        "jun, "
        "jul, "
        "aug, "
        "sep, "
        "oct, "
        "nov, "
        '"dec", '
        "jan, "
        "feb, "
        "mar, "
        "adj1, "
        "adj2, "
        "adj3, "
        "financial_code_id, "
        "financial_year_id "
        "FROM previous_years_archivedforecastdataupload;"
    )

    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
    financial_year_obj = FinancialYear.objects.get(pk=year)
    financial_year_obj.archived = True
    financial_year_obj.archived_at = datetime.datetime.now()
    financial_year_obj.save()


def upload_previous_year_figures(
    previous_year_row, financial_year_obj, financialcode_obj, header_dict
):
    new_values = {}
    value_found = False

    for month_name in DATA_HEADERS:
        month_amount = previous_year_row[header_dict[month_name]].value
        if month_amount is None or month_amount == "-":
            # we accept the '-' as it is a recognised value in Finance for 0
            month_amount = 0
        else:
            try:
                month_amount = month_amount * 100
            except ValueError:
                raise UploadFileFormatError(
                    f"Non-numeric value in {month_name}:{month_amount}"
                )
        if month_amount:
            value_found = True
        new_values[month_name] = month_amount

    if value_found:
        (
            previous_year_obj,
            created,
        ) = ArchivedForecastDataUpload.objects.get_or_create(
            financial_year=financial_year_obj, financial_code=financialcode_obj,
        )
        # to avoid problems with precision,
        # we store the figures in pence
        if created:
            previous_year_obj.budget = new_values["budget"]
            previous_year_obj.apr = new_values["apr"]
            previous_year_obj.may = new_values["may"]
            previous_year_obj.jun = new_values["jun"]
            previous_year_obj.jul = new_values["jul"]
            previous_year_obj.aug = new_values["aug"]
            previous_year_obj.sep = new_values["sep"]
            previous_year_obj.oct = new_values["oct"]
            previous_year_obj.nov = new_values["nov"]
            previous_year_obj.dec = new_values["dec"]
            previous_year_obj.jan = new_values["jan"]
            previous_year_obj.feb = new_values["feb"]
            previous_year_obj.mar = new_values["mar"]
            previous_year_obj.adj1 = new_values["adj01"]
            previous_year_obj.adj2 = new_values["adj02"]
            previous_year_obj.adj3 = new_values["adj03"]
        else:
            previous_year_obj.budget += new_values["budget"]
            previous_year_obj.apr += new_values["apr"]
            previous_year_obj.may += new_values["may"]
            previous_year_obj.jun += new_values["jun"]
            previous_year_obj.jul += new_values["jul"]
            previous_year_obj.aug += new_values["aug"]
            previous_year_obj.sep += new_values["sep"]
            previous_year_obj.oct += new_values["oct"]
            previous_year_obj.nov += new_values["nov"]
            previous_year_obj.dec += new_values["dec"]
            previous_year_obj.jan += new_values["jan"]
            previous_year_obj.feb += new_values["feb"]
            previous_year_obj.mar += new_values["mar"]
            previous_year_obj.adj1 += new_values["adj01"]
            previous_year_obj.adj2 += new_values["adj02"]
            previous_year_obj.adj3 += new_values["adj03"]
        previous_year_obj.save()


def upload_previous_year(worksheet, financial_year, file_upload):  # noqa
    header_dict = xslx_header_to_dict(worksheet[1])
    expected_headers = [
        COST_CENTRE_HEADER,
        NAC_HEADER,
        PROGRAMME_HEADER,
        ANALYSIS_HEADER,
        ANALYSIS2_HEADER,
        PROJECT_HEADER,
    ]
    expected_headers.extend(DATA_HEADERS)
    check_header(header_dict, expected_headers)

    try:
        validate_year_for_archiving_actuals(financial_year)
    except ArchiveYearError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        raise ex

    financial_year_obj = FinancialYear.objects.get(pk=financial_year)

    # Clear the table used to upload the previous_years.
    # The previous_years are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    ArchivedForecastDataUpload.objects.filter(financial_year=financial_year,).delete()
    rows_to_process = worksheet.max_row + 1

    check_financial_code = CheckArchivedFinancialCode(financial_year, file_upload)
    cc_index = header_dict[COST_CENTRE_HEADER]
    nac_index = header_dict[NAC_HEADER]
    prog_index = header_dict[PROGRAMME_HEADER]
    a1_index = header_dict[ANALYSIS_HEADER]
    a2_index = header_dict[ANALYSIS2_HEADER]
    proj_index = header_dict[PROJECT_HEADER]
    row_number = 0
    # There is a terrible performance hit accessing the individual cells:
    # The cell is found starting from cell A0, and continuing until the
    # required cell is found
    # The rows in worksheet.rows are accessed sequentially, so there is no
    # performance problem.
    # A typical files took over 2 hours to read using the cell access method
    # and 10 minutes with the row access.
    for previous_year_row in worksheet.rows:
        row_number += 1
        if row_number == 1:
            # There is no way to start reading rows from a specific place.
            # Ignore first row, the headers have been processed already
            continue
        if not row_number % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                file_upload, f"Processing row {row_number} of {rows_to_process}."
            )
        cost_centre = previous_year_row[cc_index].value
        if not cost_centre:
            # protection against empty rows
            break
        nac = previous_year_row[nac_index].value
        programme_code = previous_year_row[prog_index].value
        analysis1 = previous_year_row[a1_index].value
        analysis2 = previous_year_row[a2_index].value
        project_code = previous_year_row[proj_index].value
        check_financial_code.validate(
            cost_centre,
            nac,
            programme_code,
            analysis1,
            analysis2,
            project_code,
            row_number,
        )
        if not check_financial_code.error_found:
            financialcode_obj = check_financial_code.get_financial_code()
            try:
                upload_previous_year_figures(
                    previous_year_row,
                    financial_year_obj,
                    financialcode_obj,
                    header_dict,
                )
            except (UploadFileFormatError, ArchiveYearError) as ex:
                set_file_upload_fatal_error(
                    file_upload, str(ex), str(ex),
                )
                raise ex

    final_status = FileUpload.PROCESSED
    if check_financial_code.error_found:
        final_status = FileUpload.PROCESSEDWITHERROR
    else:
        # No errors, so we can copy the figures
        # from the temporary table to the previous_years
        copy_uploaded_previous_year(financial_year)
        if check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )

    if check_financial_code.error_found:
        raise UploadFileDataError(
            "No data uploaded. Check the log in the file upload record."
        )


def upload_previous_year_from_file(file_upload, year):
    try:
        workbook, worksheet = validate_excel_file(file_upload, VALID_WS_NAME)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        raise ex
    try:
        upload_previous_year(worksheet, year, file_upload)
    except (UploadFileDataError, ArchiveYearError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    workbook.close
