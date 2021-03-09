import logging

from core.models import FinancialYear

from forecast.utils.import_helpers import (
    UploadFileDataError,
    UploadFileFormatError,
)
from forecast.utils.query_fields import ForecastQueryFields

from previous_years.import_previous_year import (
    copy_previous_year_figure_from_temp_table,
)
from previous_years.models import ArchivedForecastDataUpload
from previous_years.utils import (
    ArchiveYearError,
    CheckArchivedFinancialCode,
    validate_year_for_archiving_actuals,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)


logger = logging.getLogger(__name__)


def archive_to_temp_previous_year_figures(
    row_to_archive, financial_year_obj, financialcode_obj
):
    (previous_year_obj, created,) = ArchivedForecastDataUpload.objects.get_or_create(
        financial_year=financial_year_obj, financial_code=financialcode_obj,
    )
    # to avoid problems with precision,
    # we store the figures in pence
    if created:
        previous_year_obj.budget = row_to_archive["Budget"]
        previous_year_obj.apr = row_to_archive["Apr"]
        previous_year_obj.may = row_to_archive["May"]
        previous_year_obj.jun = row_to_archive["Jun"]
        previous_year_obj.jul = row_to_archive["Jul"]
        previous_year_obj.aug = row_to_archive["Aug"]
        previous_year_obj.sep = row_to_archive["Sep"]
        previous_year_obj.oct = row_to_archive["Oct"]
        previous_year_obj.nov = row_to_archive["Nov"]
        previous_year_obj.dec = row_to_archive["Dec"]
        previous_year_obj.jan = row_to_archive["Jan"]
        previous_year_obj.feb = row_to_archive["Feb"]
        previous_year_obj.mar = row_to_archive["Mar"]
        previous_year_obj.adj1 = row_to_archive["Adj1"]
        previous_year_obj.adj2 = row_to_archive["Adj2"]
        previous_year_obj.adj3 = row_to_archive["Adj3"]
    else:
        previous_year_obj.budget += row_to_archive["Budget"]
        previous_year_obj.apr += row_to_archive["Apr"]
        previous_year_obj.may += row_to_archive["May"]
        previous_year_obj.jun += row_to_archive["Jun"]
        previous_year_obj.jul += row_to_archive["Jul"]
        previous_year_obj.aug += row_to_archive["Aug"]
        previous_year_obj.sep += row_to_archive["Sep"]
        previous_year_obj.oct += row_to_archive["Oct"]
        previous_year_obj.nov += row_to_archive["Nov"]
        previous_year_obj.dec += row_to_archive["Dec"]
        previous_year_obj.jan += row_to_archive["Jan"]
        previous_year_obj.feb += row_to_archive["Feb"]
        previous_year_obj.mar += row_to_archive["Mar"]
        previous_year_obj.adj1 += row_to_archive["Adj1"]
        previous_year_obj.adj2 += row_to_archive["Adj2"]
        previous_year_obj.adj3 += row_to_archive["Adj3"]
    previous_year_obj.save()


def set_final_status(check_financial_code):
    final_status = FileUpload.PROCESSED
    if check_financial_code.warning_found:
        final_status = FileUpload.PROCESSEDWITHWARNING

    if check_financial_code.error_found:
        final_status = FileUpload.PROCESSEDWITHERROR

    return final_status


def archive_current_year():
    # Get the latest period for archiving
    fields = ForecastQueryFields()
    financial_year = fields.selected_year

    try:
        validate_year_for_archiving_actuals(financial_year, False)
    except ArchiveYearError as ex:
        raise ex

    datamodel = fields.datamodel
    data_to_archive_list = datamodel.view_data.raw_data_annotated(
        fields.archive_forecast_columns, {}, year=financial_year
    )
    financial_year_obj = FinancialYear.objects.get(pk=financial_year)
    # Clear the table used to upload the previous_years.
    # The previous_years are uploaded to to a temporary storage,
    # and copied when the upload is completed successfully.
    # This means that we always have a full upload.
    ArchivedForecastDataUpload.objects.filter(financial_year=financial_year,).delete()
    rows_to_process = data_to_archive_list.count()

    # Create an entry in the file upload table, even if it is not a file.
    # It is useful for keeping the log of errors
    file_upload = FileUpload(
        document_file_name="dummy",
        document_type=FileUpload.PREVIOUSYEAR,
        file_location=FileUpload.LOCALFILE,
    )

    check_financial_code = CheckArchivedFinancialCode(financial_year, file_upload)
    row_number = 0
    cost_centre_field = fields.cost_centre_code_field
    nac_field = fields.nac_code_field
    programme_field = fields.programme_code_field
    analysis1_field = fields.analysis1_code_field
    analysis2_field = fields.analysis2_code_field
    project_code_field = fields.project_code_field

    for row_to_archive in data_to_archive_list:
        row_number += 1
        if not row_number % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                file_upload, f"Processing row {row_number} of {rows_to_process}."
            )
            logger.info(f"Processing row {row_number} of {rows_to_process}.")

        cost_centre = row_to_archive[cost_centre_field]
        nac = row_to_archive[nac_field]
        programme_code = row_to_archive[programme_field]
        analysis1 = row_to_archive[analysis1_field]
        analysis2 = row_to_archive[analysis2_field]
        project_code = row_to_archive[project_code_field]

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
                archive_to_temp_previous_year_figures(
                    row_to_archive, financial_year_obj, financialcode_obj,
                )
            except (UploadFileFormatError, ArchiveYearError) as ex:
                set_file_upload_fatal_error(
                    file_upload, str(ex), str(ex),
                )
                raise ex

    final_status = set_final_status(check_financial_code)

    if final_status != FileUpload.PROCESSEDWITHERROR:
        # No errors, so we can copy the figures
        # from the temporary table to the previous_years
        copy_previous_year_figure_from_temp_table(financial_year)

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )

    if final_status == FileUpload.PROCESSEDWITHERROR:
        raise UploadFileDataError(
            "No data archived. Check the log in the file upload record."
        )
