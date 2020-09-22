from chartofaccountDIT.models import ArchivedAnalysis1

from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    IMPORT_CSV_PK_NAME_KEY,
    import_obj,
)

from forecast.import_csv import WrongChartOFAccountCodeException

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


def import_archived_analysis1(csvfile, year):
    success, msg = import_obj(csvfile, ANALYSIS1_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(
            f"Importing archived Analysis1 (Contract) error: " f"{msg}"
        )
    return success, msg
