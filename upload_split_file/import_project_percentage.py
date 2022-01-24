from django.db import connection
from django.db.models import Sum

from core.import_csv import xslx_header_to_dict

from end_of_month.models import EndOfMonthStatus

from forecast.models import FinancialPeriod
from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileDataError,
    UploadFileFormatError,
    check_header,
    validate_excel_file,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

from upload_split_file.models import (
    PaySplitCoefficient,
    UploadPaySplitCoefficient,
)
from upload_split_file.split_actuals import (
    PAY_CODE,
    handle_split_project,
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
TOLERANCE = 100


class UploadProjectPercentages:
    def __init__(
        self,
        worksheet,
        header_dict,
        file_upload,
        expenditure_type,
        include_archived=False,
    ):
        self.worksheet = worksheet
        self.cc_index = header_dict[COST_CENTRE_CODE]
        self.nac_index = header_dict[NAC_CODE]
        self.prog_index = header_dict[PROGRAMME_CODE]
        self.a1_index = header_dict[ANALYSIS1_CODE]
        self.a2_index = header_dict[ANALYSIS2_CODE]
        self.proj_index = header_dict[PROJECT_CODE]
        self.file_upload = file_upload
        self.rows_to_process = self.worksheet.max_row + 1
        self.include_archived = include_archived
        self.expenditure_type = expenditure_type
        self.directorate_code = ""
        self.create_month_dict(header_dict)

    def create_month_dict(self, header_dict):
        # Not all months are available in the excel file
        # And we are only able to change month that have not yet been archived.
        # Also, we may have the case of a month header, and no data in the columns
        self.month_dict = {}
        self.month_data_found_dict = {}
        if self.include_archived:
            month_queryset = FinancialPeriod.objects.all()
        else:
            max_archived_period = (
                EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
            )
            month_queryset = FinancialPeriod.objects.filter(
                financial_period_code__gt=max_archived_period
            )

        for month in month_queryset:
            month_name = month.period_short_name.lower()
            if month_name in header_dict:
                self.month_dict[header_dict[month_name]] = month
                self.month_data_found_dict[header_dict[month_name]] = False
        if not self.month_dict:
            raise UploadFileFormatError("Error: no period specified.\n")

    def display_row_count(self):
        if not self.current_row % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                self.file_upload,
                f"Processing row {self.current_row} of {self.rows_to_process}.",
            )

    def final_checks(self):
        if (
            self.check_financial_code.error_found
            or self.check_financial_code.non_fatal_error_found
        ):
            raise UploadFileDataError("Errors found. Upload aborted.\n")

        # No errors, but check that are data to be used
        for month_idx, month_info in self.month_data_found_dict.items():
            if not month_info:
                del self.month_dict[month_idx]
        if not self.month_dict:
            raise UploadFileDataError(
                "Error: no data specified.\nUpload aborted: Data error.\n",
            )

    def copy_uploaded_percentage(self):
        for period_obj in self.month_dict.values():
            # Now copy the newly uploaded budgets to the monthly figure table
            PaySplitCoefficient.objects.filter(financial_period=period_obj,).delete()
            sql_insert = (
                f"INSERT INTO public.upload_split_file_paysplitcoefficient "
                f"(created, updated, "
                f"split_coefficient, directorate_code, "
                f"financial_code_to_id, financial_period_id)	"
                f"SELECT now(), now(), "
                f"split_coefficient, directorate_code, "
                f"financial_code_to_id, financial_period_id "
                f"FROM public.upload_split_file_uploadpaysplitcoefficient "
                f"WHERE financial_period_id = "
                f"{period_obj.financial_period_code};"
            )
            with connection.cursor() as cursor:
                cursor.execute(sql_insert)
            UploadPaySplitCoefficient.objects.filter(
                financial_period=period_obj,
            ).delete()

    def get_valid_percentage_value(self, period_percentage):
        # We import from Excel, and the user
        # may have entered spaces in an empty cell.
        if type(period_percentage) == str:
            period_percentage = period_percentage.strip()
        if period_percentage == "-":
            # we accept the '-' as it is a recognised value in Finance for 0
            period_percentage = 0
        try:
            # there is a numeric value for this month.
            period_percentage = round(period_percentage * MAX_COEFFICIENT)
        except ValueError:
            raise UploadFileDataError("Non-numeric value")
        # if period_percentage < 0:
        #     raise UploadFileDataError("Negative value")

        if period_percentage > MAX_COEFFICIENT:
            raise UploadFileDataError("Value higher than 100%")
        return period_percentage

    def upload_project_percentage_row(self, percentage_row):
        financialcode_obj = self.check_financial_code.get_financial_code()
        if not self.directorate_code:
            self.directorate_code = (
                financialcode_obj.cost_centre.directorate.directorate_code
            )
            self.directorate_name = (
                financialcode_obj.cost_centre.directorate.directorate_name
            )

        if (
            financialcode_obj.cost_centre.directorate.directorate_code
            != self.directorate_code
        ):
            err_msg = (
                f"Cost centre '{financialcode_obj.cost_centre.cost_centre_code}' "
                f"is not part of directorate "
                f"{self.directorate_code} - {self.directorate_name}.\n"
            )
            self.check_financial_code.record_error(self.current_row, err_msg, False)
            return

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

            if period_percentage and financialcode_obj:
                self.month_data_found_dict[month_idx] = True
                (
                    percentage_obj,
                    created,
                ) = UploadPaySplitCoefficient.objects.get_or_create(
                    financial_period=month_obj,
                    financial_code_to=financialcode_obj,
                    directorate_code=self.directorate_code,
                )
                if created:
                    percentage_obj.split_coefficient = period_percentage
                else:
                    percentage_obj.split_coefficient += period_percentage
                percentage_obj.row_number = self.current_row
                percentage_obj.save()

    def apply_percentages(self):
        for month_obj in self.month_dict.values():
            if month_obj.actual_loaded:
                handle_split_project(month_obj.financial_period_code)

    def validate_percentages(self):
        error_found = False
        error_msg = ""
        for month_obj in self.month_dict.values():
            total_percentage = UploadPaySplitCoefficient.objects.filter(
                directorate_code=self.directorate_code, financial_period=month_obj,
            ).aggregate(Sum("split_coefficient"))
            if total_percentage["split_coefficient__sum"] > MAX_COEFFICIENT + TOLERANCE:
                error_msg = (
                    f"{error_msg}The sum of the percentages is higher "
                    f"than 100% for {month_obj.period_long_name}.\n"
                )
                error_found = True
            if total_percentage["split_coefficient__sum"] < MAX_COEFFICIENT - TOLERANCE:
                error_msg = (
                    f"{error_msg}The sum of the percentages is lower "
                    f"than 100% for  {month_obj.period_long_name}.\n"
                )
                error_found = True
        if error_found:
            raise UploadFileDataError(error_msg)

    def complete(self):
        final_status = FileUpload.PROCESSED
        if (
            self.check_financial_code.error_found
            or self.check_financial_code.non_fatal_error_found
        ):
            final_status = FileUpload.PROCESSEDWITHERROR
        elif self.check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING
        set_file_upload_feedback(
            self.file_upload, f"Processed {self.current_row} rows.", final_status
        )

    def read_percentages(self):
        # Clear the table used to upload the percentages.
        # The percentages are uploaded to to a temporary storage, and copied
        # when the upload is completed successfully.
        # This means that we always have a full upload.
        UploadPaySplitCoefficient.objects.all().delete()
        self.check_financial_code = CheckFinancialCode(
            self.file_upload, self.expenditure_type
        )
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
            if not self.check_financial_code.error_found:
                self.upload_project_percentage_row(percentage_row)
        self.final_checks()


def upload_project_percentage_from_file(worksheet, file_upload, include_archived=False):
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_header(header_dict, EXPECTED_PERCENTAGE_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        return

    try:
        upload = UploadProjectPercentages(
            worksheet, header_dict, file_upload, PAY_CODE, include_archived,
        )
        upload.read_percentages()
        upload.validate_percentages()
        upload.copy_uploaded_percentage()
        upload.apply_percentages()

    except (UploadFileDataError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
    upload.complete()


def upload_project_percentage(file_upload, include_archived=False):
    try:
        workbook, worksheet = validate_excel_file(file_upload, WORKSHEET_PROJECT_TITLE)
    except (UploadFileFormatError, UploadFileDataError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        return
    upload_project_percentage_from_file(worksheet, file_upload, include_archived)
    workbook.close
