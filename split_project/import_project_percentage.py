from django.db import connection
from django.db.models import Sum

from core.import_csv import xslx_header_to_dict

from end_of_month.models import EndOfMonthStatus

from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileDataError,
    UploadFileFormatError,
    check_header,
    validate_excel_file,
)

from split_project.models import (
    ProjectSplitCoefficient,
    UploadProjectSplitCoefficient,
)
from split_project.split_figure import handle_split_project

from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

WORKSHEET_PROJECT_TITLE = "Project Percentages"
COST_CENTRE_CODE = "cost centre code"
NAC_CODE = "natural account code"
PROGRAMME_CODE = "programme code"
PROJECT_CODE = "project code"
ANALYSIS1_CODE = "contract code"
ANALYSIS2_CODE = "market code"
EXPECTED_PERCENTAGE_HEADERS = [
    COST_CENTRE_CODE,
    NAC_CODE,
    PROGRAMME_CODE,
    ANALYSIS1_CODE,
    ANALYSIS2_CODE,
    PROJECT_CODE,
]

# The percentages are stored as integers in the database.
# We allow 2 decimal figures, like 20.12%
# So to get an integer we need to multiply the float point in the file by 10000
MAX_COEFFICIENT = 10000


class UploadProjectPercentages:
    def __init__(self, worksheet, header_dict, file_upload):
        self.worksheet = worksheet
        self.cc_index = header_dict[COST_CENTRE_CODE]
        self.nac_index = header_dict[NAC_CODE]
        self.prog_index = header_dict[PROGRAMME_CODE]
        self.a1_index = header_dict[ANALYSIS1_CODE]
        self.a2_index = header_dict[ANALYSIS2_CODE]
        self.proj_index = header_dict[PROJECT_CODE]
        self.file_upload = file_upload
        self.row_to_process = self.worksheet.max_row + 1
        self.create_month_dict(header_dict)

    def create_month_dict(self, header_dict):
        # Not all months are available in the excel file
        # And we are only able to change month that have not yet been archived.
        # Also, we may have the case of a month header, and no data in the columns
        self.month_dict = {}
        self.month_data_found_dict = {}
        for month in EndOfMonthStatus.objects.filter(archived=False):
            month_name = month.archived_period.period_short_name.lower()
            if month_name in header_dict:
                self.month_dict[header_dict[month_name]] = month.archived_period
                self.month_data_found_dict[header_dict[month_name]] = False
        if not self.month_dict:
            raise UploadFileFormatError("Error: no period specified.\n")

    def display_row_count(self):
        if not self.current_row % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                self.file_upload,
                f"Processing row {self.current_row} " f"of {self.rows_to_process}.",
            )

    def final_checks(self):
        if (
            self.check_financial_code.error_found
            or self.check_financial_code.non_fatal_error_found
        ):
            raise UploadFileDataError("Error founds. Upload aborted.\n")

        # No errors, but check that are data to be used
        for month_idx, month_info in self.month_data_found_dict.items():
            if not month_info:
                del self.month_dict[month_idx]
        if not self.month_dict:
            raise UploadFileDataError(
                "Error: no data specified.\n", "Upload aborted: Data error.\n",
            )

    def copy_uploaded_percentage(self):
        for period_obj in self.month_dict.values():
            # Now copy the newly uploaded budgets to the monthly figure table
            ProjectSplitCoefficient.objects.filter(
                financial_period=period_obj,
            ).delete()
            sql_insert = (
                f"INSERT INTO public.split_project_projectsplitcoefficient"
                f"(created, updated, "
                f"split_coefficient, financial_code_from_id, "
                f"financial_code_to_id, financial_period_id)	"
                f"SELECT now(), now(), "
                f"split_coefficient, financial_code_from_id, "
                f"financial_code_to_id, financial_period_id "
                f"FROM public.split_project_uploadprojectsplitcoefficient "
                f"WHERE financial_period_id = "
                f"{period_obj.financial_period_code};"
            )
            with connection.cursor() as cursor:
                cursor.execute(sql_insert)
            UploadProjectSplitCoefficient.objects.filter(
                financial_period=period_obj,
            ).delete()

    def save_month_percentage(self):
        pass

    def get_valid_percentage_value(self, period_percentage):
        # We import from Excel, and the user
        # may have entered spaces in an empty cell.
        if type(period_percentage) == str:
            period_percentage = period_percentage.strip()
        if period_percentage == "-":
            # we accept the '-' as it is a recognised value in Finance for 0
            period_percentage = 0
        try:
            period_percentage = int(period_percentage * MAX_COEFFICIENT)
            # there is a numeric value for this month.
        except ValueError:
            raise UploadFileDataError("Non-numeric value")
        if period_percentage < 0:
            raise UploadFileDataError("Negative value")

        if period_percentage > MAX_COEFFICIENT:
            raise UploadFileDataError("Value higher than 100%")
        return period_percentage

    def upload_project_percentage_row(self, percentage_row):
        for month_idx, month_obj in self.month_dict.items():
            period_percentage = percentage_row[month_idx].value
            if period_percentage is None:
                continue
            try:
                period_percentage = self.get_valid_percentage_value(period_percentage)
            except UploadFileDataError as ex:
                err_msg = f"{str(ex)} in cell {percentage_row[month_idx].coordinate}.\n"
                self.check_financial_code.record_error(self.current_row, err_msg, False)
                continue

            if period_percentage:
                self.month_data_found_dict[month_idx] = True
                financialcode_obj_to = self.check_financial_code.get_financial_code()
                financialcode_obj_from = (
                    self.check_financial_code.get_financial_code_no_project()
                )
                (
                    percentage_obj,
                    created,
                ) = UploadProjectSplitCoefficient.objects.get_or_create(
                    financial_period=month_obj,
                    financial_code_from=financialcode_obj_from,
                    financial_code_to=financialcode_obj_to,
                )
                if created:
                    percentage_obj.split_coefficient = period_percentage
                    percentage_obj.row_number = self.current_row
                    percentage_obj.save()
                else:
                    err_msg = (
                        f"Chart of account data "
                        f"in row {self.current_row} "
                        f"is a duplicate of "
                        f"{percentage_obj.row_number}.\n"
                    )
                    self.check_financial_code.record_error(
                        self.current_row, err_msg, False
                    )

    def apply_percentages(self):
        for month_obj in self.month_dict.values():
            if month_obj.actual_loaded:
                handle_split_project(month_obj.financial_period_code)

    def validate_percentages(self):
        total_queryset = (
            UploadProjectSplitCoefficient.objects.values(
                "financial_period",
                "financial_period__period_long_name",
                "financial_code_from",
            )
            .annotate(percentage=Sum("split_coefficient"))
            .filter(percentage__gte=MAX_COEFFICIENT)
        )
        if total_queryset:
            err_msg = ""
            for code in total_queryset:
                row_list = (
                    UploadProjectSplitCoefficient.objects.filter(
                        financial_period=code["financial_period"],
                        financial_code_from=code["financial_code_from"],
                    )
                    .order_by("row_number")
                    .values_list("row_number", flat=True)
                )

                err_msg = (
                    f"{err_msg}The sum of percentages in rows {list(row_list)} "
                    f"for {code['financial_period__period_long_name']} "
                    f"is greater than 100%.\n"
                )
        raise UploadFileDataError(f"{err_msg}")

    def read_percentages(self):
        # Clear the table used to upload the percentages.
        # The percentages are uploaded to to a temporary storage, and copied
        # when the upload is completed successfully.
        # This means that we always have a full upload.
        UploadProjectSplitCoefficient.objects.all().delete()
        self.check_financial_code = CheckFinancialCode(self.file_upload)
        self.current_row = 0
        for percentage_row in self.worksheet.rows:
            self.current_row += 1
            if self.current_row == 1:
                # There is no way to start reading rows from a specific place.
                # Ignore first row, the headers have been processed already
                continue
            self.display_row_count()
            cost_centre = percentage_row[self.cc_index].value
            if not cost_centre:
                # protection against empty rows
                break
            self.check_financial_code.validate(
                cost_centre,
                percentage_row[self.nac_index].value,
                percentage_row[self.prog_index].value,
                percentage_row[self.a1_index].value,
                percentage_row[self.a2_index].value,
                percentage_row[self.proj_index].value,
                self.current_row,
            )
            self.upload_project_percentage_row(percentage_row)
        self.final_checks()


def upload_project_percentage_from_file(file_upload):
    try:
        workbook, worksheet = validate_excel_file(file_upload, WORKSHEET_PROJECT_TITLE)
    except (UploadFileFormatError, UploadFileDataError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        return
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_header(header_dict, EXPECTED_PERCENTAGE_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        return

    try:
        upload = UploadProjectPercentages(worksheet, header_dict, file_upload)
        upload.read_percentages()
        upload.validate_percentages()
        upload.copy_uploaded_percentage()
        upload.apply_percentages()

    except (UploadFileDataError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
    workbook.close
