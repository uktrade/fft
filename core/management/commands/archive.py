from django.core.management.base import BaseCommand

from chartofaccountDIT.archive import (
    archive_all,
    archive_analysis_1,
    archive_analysis_2,
    archive_commercial_category,
    archive_expenditure_category,
    archive_fco_mapping,
    archive_inter_entity,
    archive_natural_code,
    archive_programme_code,
    archive_project_code,
)

from costcentre.archive import archive_cost_centre

from treasuryCOA.archive import archive_treasury_l5

ARCHIVE_TYPE = {
    "CostCentre": archive_cost_centre,
    "Treasury_COA": archive_treasury_l5,
    "Programmes": archive_programme_code,
    "NAC": archive_natural_code,
    "Analysis1": archive_analysis_1,
    "Analysis2": archive_analysis_2,
    "Expenditure_Cat": archive_expenditure_category,
    "FCO_mapping": archive_fco_mapping,
    "Commercial_Cat": archive_commercial_category,
    "Inter_entity": archive_inter_entity,
    "Project_Code": archive_project_code,
}


class Command(BaseCommand):
    help = (
        "archive element of Chart of Account. "
        "Allowed types are - All - {} - ".format(" - ".join(ARCHIVE_TYPE.keys()))
    )

    def add_arguments(self, parser):
        parser.add_argument("type")
        parser.add_argument("year", type=int, nargs="?", default=2018)

    # pass the year an argument
    def handle(self, *args, **options):
        financialyear = options.get("year")
        archivetype = options.get("type")
        if archivetype == "All":
            archive_all(financialyear)
            archive_cost_centre(financialyear)
            archive_treasury_l5(financialyear)
        else:
            row = ARCHIVE_TYPE[archivetype](financialyear)
            print("Archived " + str(row) + " rows")
