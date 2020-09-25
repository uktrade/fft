from django.db import connection

from chartofaccountDIT.import_csv import BUDGET_KEY
from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedExpenditureCategory,
    ArchivedNaturalCode,
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
    IMPORT_CSV_FIELDLIST_KEY: {"analysis2_description": "Market Description", },
}

PROJECT_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedProjectCode,
    IMPORT_CSV_PK_KEY: "Project Code",
    IMPORT_CSV_PK_NAME_KEY: "project_code",
    IMPORT_CSV_FIELDLIST_KEY: {"project_description": "Project Description"},
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


EXPENDITURE_CATEGORY_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedExpenditureCategory,
    IMPORT_CSV_PK_KEY: "Budget Category",
    IMPORT_CSV_PK_NAME_KEY: "grouping_description",
    IMPORT_CSV_FIELDLIST_KEY: {"NAC_category_description": "Budget Grouping"},
}


NAC_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedNaturalCode,
    IMPORT_CSV_PK_NAME_KEY: "natural_account_code",
    IMPORT_CSV_PK_KEY: "Natural Account",
    IMPORT_CSV_FIELDLIST_KEY: {
        "natural_account_code_description": "NAC desc",
        "NAC_category": "Budget Grouping",
        "economic_budget_code": "Expenditure Type",
        "expenditure_category": EXPENDITURE_CATEGORY_HISTORICAL_KEY,
    },
}


def import_archived_analysis1(csvfile, year):
    msgerror = "Failure importing archived Analysis 1. Error:"
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(f"{msgerror} {str(ex)}")
    success, msg = import_obj(csvfile, ANALYSIS1_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(f"{msgerror} {msg}")
    return success, msg


def import_archived_analysis2(csvfile, year):
    msgerror = "Failure importing archived Analysis 2. Error:"
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(f"{msgerror} {str(ex)}")
    success, msg = import_obj(csvfile, ANALYSIS2_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(f"{msgerror} {msg}")
    return success, msg


def import_archived_project(csvfile, year):
    msgerror = "Failure importing archived Project. Error:"
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(f"{msgerror} {str(ex)}")
    success, msg = import_obj(csvfile, PROJECT_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(f"{msgerror} {msg}")
    return success, msg


def import_archived_programme(csvfile, year):
    msgerror = "Failure importing archived Programme. Error:"
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(f"{msgerror} {str(ex)}")
    success, msg = import_obj(csvfile, PROGRAMME_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(f"{msgerror} {msg}")
    return success, msg


def import_archived_nac(csvfile, year):
    msgerror = "Failure importing archived NAC. Error:"
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(f"{msgerror} {str(ex)}")
    success, msg = import_obj(csvfile, NAC_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(f"{msgerror} {msg}")
        # Use sql to initialise the NAC_Category_id foreign key in the archived table
        # this code will not be used in future, so it is not important
        # to make maintainable
        with connection.cursor() as cursor:
            cursor.execute(
                'update "chartofaccountDIT_archivedexpenditurecategory" '
                'SET "NAC_category_id" = a.id '
                'FROM "chartofaccountDIT_naccategory" a '
                'WHERE a."NAC_category_description" = '
                '"chartofaccountDIT_archivedexpenditurecategory"."NAC_category_description";'  # noqa
            )
    return success, msg
