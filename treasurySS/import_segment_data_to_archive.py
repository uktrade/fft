import csv

from chartofaccountDIT.models import BudgetType

from core.import_csv import csv_header_to_dict

from treasurySS.models import ArchivedSubSegment

from previous_years.utils import (
    ArchiveYearError,
    validate_year_for_archiving,
)

SUB_SEGMENT_CODE_HEADER = "sub segment code"
SUB_SEGMENT_LONG_NAME_HEADER = "sub segment long name"
CONTROL_BUDGET_DETAIL_CODE_HEADER = "control budget detail code"
ACCOUNTING_AUTHORITY_CODE_HEADER = "accounting authority code"
ACCOUNTING_AUTHORITY_DETAILCODE_HEADER = "accounting authority detail code"
DIT_BUDGET_TYPE_HEADER = "dit budget code (used to generate the oscar return)"
SEGMENT_GRAND_PARENT_CODE_HEADER = "segment grand parent code"
SEGMENT_GRAND_PARENT_LONG_NAME_HEADER = "segment grand parent long name"
SEGMENT_DEPARTMENT_CODE_HEADER = "department code"
SEGMENT_DEPARTMENT_LONG_NAME_HEADER = "department long name"
SEGMENT_PARENT_CODE_HEADER = "segment parent code"
SEGMENT_PARENT_LONG_NAME_HEADER = "segment parent long name"
SEGMENT_CODE_HEADER = "segment code"
SEGMENT_LONG_NAME_HEADER = "segment long name"
ORGANIZATION_CODE_HEADER = "organisation"
ORGANIZATION_ALIAS_HEADER = "organisation alias"
ESTIMATE_ROW_CODE_HEADER = "estimates row code"
ESTIMATE_ROW_LONG_NAME_HEADER = "estimates row long name"

header_expected = [
    SUB_SEGMENT_CODE_HEADER,
    SUB_SEGMENT_LONG_NAME_HEADER,
    CONTROL_BUDGET_DETAIL_CODE_HEADER,
    ACCOUNTING_AUTHORITY_CODE_HEADER,
    ACCOUNTING_AUTHORITY_DETAILCODE_HEADER,
    DIT_BUDGET_TYPE_HEADER,
    SEGMENT_GRAND_PARENT_CODE_HEADER,
    SEGMENT_GRAND_PARENT_LONG_NAME_HEADER,
    SEGMENT_DEPARTMENT_CODE_HEADER,
    SEGMENT_DEPARTMENT_LONG_NAME_HEADER,
    SEGMENT_PARENT_CODE_HEADER,
    SEGMENT_PARENT_LONG_NAME_HEADER,
    SEGMENT_CODE_HEADER,
    SEGMENT_LONG_NAME_HEADER,
    ORGANIZATION_CODE_HEADER,
    ORGANIZATION_ALIAS_HEADER,
    ESTIMATE_ROW_CODE_HEADER,
    ESTIMATE_ROW_LONG_NAME_HEADER,
]


class WrongHeaderException(Exception):
    pass


def import_segment(csv_file, year):
    reader = csv.reader(csv_file)
    header = csv_header_to_dict(next(reader))

    missing_headers = []
    # "Before starting to read, check that all the expected columns exists
    for elem in header_expected:
        if elem not in header:
            missing_headers.append(elem)

    if missing_headers:
        raise WrongHeaderException(
            f"Missing/wrong headers: expected {header_expected}, "
            f"missing {missing_headers}."
        )

    # Clear existing segment data
    ArchivedSubSegment.objects.filter(financial_year_id=year).delete()
    row_number = 1

    for row in reader:
        row_number = row_number + 1
        # protection against empty rows
        if len(row) == 0:
            break

        sub_segment_code = row[header[SUB_SEGMENT_CODE_HEADER]].strip()
        obj, _ = ArchivedSubSegment.objects.get_or_create(
            sub_segment_code=sub_segment_code, financial_year_id=year
        )

        obj.sub_segment_long_name = row[
            header[SUB_SEGMENT_LONG_NAME_HEADER]
        ].strip()

        obj.control_budget_detail_code = row[
            header[CONTROL_BUDGET_DETAIL_CODE_HEADER]
        ].strip()
        obj.accounting_authority_code = row[
            header[ACCOUNTING_AUTHORITY_CODE_HEADER]
        ].strip()
        obj.accounting_authority_DetailCode = row[
            header[ACCOUNTING_AUTHORITY_DETAILCODE_HEADER]
        ].strip()
        dit_budget_type = row[header[DIT_BUDGET_TYPE_HEADER]].strip()

        if dit_budget_type and dit_budget_type != "-":
            dit_budget_type_queryset = BudgetType.objects.filter(
                budget_type=dit_budget_type
            )
            if dit_budget_type_queryset:
                obj.dit_budget_type = dit_budget_type_queryset.first()

        obj.segment_grand_parent_code = row[
            header[SEGMENT_GRAND_PARENT_CODE_HEADER]
        ].strip()
        obj.segment_grand_parent_long_name = row[
            header[SEGMENT_GRAND_PARENT_LONG_NAME_HEADER]
        ].strip()
        obj.segment_department_code = row[
            header[SEGMENT_DEPARTMENT_CODE_HEADER]
        ].strip()
        obj.segment_department_long_name = row[
            header[SEGMENT_DEPARTMENT_LONG_NAME_HEADER]
        ].strip()
        obj.segment_parent_code = row[header[SEGMENT_PARENT_CODE_HEADER]].strip()
        obj.segment_parent_long_name = row[
            header[SEGMENT_PARENT_LONG_NAME_HEADER]
        ].strip()
        obj.segment_code = row[header[SEGMENT_CODE_HEADER]].strip()
        obj.segment_long_name = row[header[SEGMENT_LONG_NAME_HEADER]].strip()
        obj.organization_code = row[header[ORGANIZATION_CODE_HEADER]].strip()
        obj.organization_alias = row[header[ORGANIZATION_ALIAS_HEADER]].strip()
        obj.estimate_row_code = row[header[ESTIMATE_ROW_CODE_HEADER]].strip()
        obj.estimate_row_long_name = row[header[ESTIMATE_ROW_LONG_NAME_HEADER]].strip()
        obj.save()


def import_segment_data(csvfile, year):
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(
            f"Error importing historical segment data. " f"Error: {str(ex)}"
        )
    try:
        import_segment(csvfile, year)
    except WrongHeaderException as ex:
        raise WrongHeaderException(
            f"Error importing historical segment data: {str(ex)}"
        )
