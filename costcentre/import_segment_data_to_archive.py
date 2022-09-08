import csv

from core.import_csv import csv_header_to_dict
from costcentre.models import ArchivedCostCentre
from previous_years.utils import ArchiveYearError, validate_year_for_archiving
from treasurySS.import_segment_data_to_archive import WrongHeaderException

SEGMENT_HEADER = "treasury segment"
DG_GROUP_HEADER = "group"


def import_segment_group(csv_file, year):
    reader = csv.reader(csv_file)
    header = csv_header_to_dict(next(reader))
    header_expected = [SEGMENT_HEADER, DG_GROUP_HEADER]

    # Before starting to read, check that all the expected columns exists
    if not all(elem in header for elem in header_expected):
        raise WrongHeaderException(
            f"Missing/wrong headers: expected {header_expected}, "
            f"the file has: {header.keys()}."
        )

    # Clear existing segment data
    ArchivedCostCentre.objects.filter(financial_year_id=year).update(
        treasury_segment_code=""
    )
    row_number = 1
    for row in reader:
        row_number = row_number + 1
        # protection against empty rows
        if len(row) == 0:
            break
        segment_code_description = row[header[SEGMENT_HEADER]].strip()
        segment_code = segment_code_description[:8]
        group_code = row[header[DG_GROUP_HEADER]].strip()
        ArchivedCostCentre.objects.filter(
            financial_year_id=year, group_code=group_code
        ).update(treasury_segment_code=segment_code)


def import_segment_group_data(csvfile, year):
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(
            f"Failure importing segment data to the cost centre hierarchy. "
            f"Error: {str(ex)}"
        )
    try:
        import_segment_group(csvfile, year)
    except WrongHeaderException as ex:
        raise WrongHeaderException(
            f"Error importing segment to archived Cost Centre hierarchy: {str(ex)}"
        )
