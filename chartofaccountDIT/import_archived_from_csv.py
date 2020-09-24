from chartofaccountDIT.import_csv import BUDGET_KEY
from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    IMPORT_CSV_PK_NAME_KEY,
    import_obj,
)

from forecast.import_csv import WrongChartOFAccountCodeException

from previous_years.utils import (
    ArchiveYearError,
    validate_year_for_archiving,
)


ANALYSIS1_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedAnalysis1,
    IMPORT_CSV_PK_KEY: "Analysis 1 Code",
    IMPORT_CSV_PK_NAME_KEY: "analysis1_code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "analysis1_description": "Contract Name",
        "supplier": "Supplier",
        "pc_reference": "PC Reference",
    },
}

ANALYSIS2_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedAnalysis2,
    IMPORT_CSV_PK_KEY: "Market Code",
    IMPORT_CSV_PK_NAME_KEY: "analysis2_code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "analysis2_description": "Market Description",
    },
}

PROJECT_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedProjectCode,
    IMPORT_CSV_PK_KEY: "Project Code",
    IMPORT_CSV_PK_NAME_KEY: "project_code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "project_description": "Project Description"
    },
}

PROGRAMME_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedProgrammeCode,
    IMPORT_CSV_PK_KEY: "Programme Code",
    IMPORT_CSV_PK_NAME_KEY: "programme_code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "programme_description": "Programme Description",
        "budget_type": BUDGET_KEY,
    },
}


def import_archived_analysis1(csvfile, year):
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(
            f"Failure import Importing archived Analysis1 (Contract) error: {str(ex)}"
        )
    success, msg = import_obj(csvfile, ANALYSIS1_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(
            f"Importing archived Analysis1 (Contract) error: " f"{msg}"
        )
    return success, msg


def import_archived_analysis2(csvfile, year):
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(
            f"Failure import Importing archived Analysis2 (Market) error: {str(ex)}"
        )
    success, msg = import_obj(csvfile, ANALYSIS2_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(
            f"Importing archived Analysis2 (Market) error: " f"{msg}"
        )
    return success, msg


def import_archived_project(csvfile, year):
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(
            f"Failure import Importing archived Project error: {str(ex)}"
        )
    success, msg = import_obj(csvfile, PROJECT_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(
            f"Importing archived Project error: " f"{msg}"
        )
    return success, msg


def import_archived_programme(csvfile, year):
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(
            f"Failure import Importing archived Programme error: {str(ex)}"
        )
    success, msg = import_obj(csvfile, PROGRAMME_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(
            f"Importing archived Programme error: " f"{msg}"
        )
    return success, msg
