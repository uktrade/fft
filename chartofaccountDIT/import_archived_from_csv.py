from django.core.exceptions import ObjectDoesNotExist

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
    IMPORT_CSV_FIELDLIST_KEY: {"analysis2_description": "Market Description"},
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
        "expenditure_category_description": "Budget Category",
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
    else:
        # The archived NAC is not normalised, and each expenditure NAC row
        # contains the corresponding budget NAC.
        # This information is missing from the upload file, so we need to extract it
        # from the expenditure category: each expenditure category row is linked to
        # a budget NAC.
        # The classification of budget and expenditure NAC is internal to DIT:
        # budgets should be set only using budget NAC, to reduce the number of lines
        nac_qs = ArchivedNaturalCode.objects.filter(financial_year=year)
        for nac_obj in nac_qs:
            if nac_obj.expenditure_category:
                account_L6_budget_val = nac_obj.expenditure_category.linked_budget_code
                nac_obj.account_L6_budget = account_L6_budget_val
                nac_obj.save()
        category_qs = ArchivedExpenditureCategory.objects.filter(financial_year=year)
        for category_obj in category_qs:
            account_L6_budget_val = category_obj.linked_budget_code
            try:
                nac_obj = ArchivedNaturalCode.objects.get(
                    financial_year=year, natural_account_code=account_L6_budget_val
                )
                nac_obj.used_for_budget = True
                nac_obj.save()
            except ObjectDoesNotExist as ex:
                msg = f"NAC {account_L6_budget_val} not defined for year {year}"
                raise WrongChartOFAccountCodeException(f"{msgerror} {msg}")

        return success, msg
