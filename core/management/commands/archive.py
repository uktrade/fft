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

from core.utils.generic_helpers import get_current_financial_year

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
        "Allowed arguments are - All - {} - ".format(" - ".join(ARCHIVE_TYPE.keys()))
    )
    arg_name = "type"

    def add_arguments(self, parser):
        parser.add_argument(self.arg_name, nargs="*", default=["All"])
        parser.add_argument("--year", type=int, nargs="?", default=0)

    # pass the year an argument
    def handle(self, *args, **options):
        financial_year = options.get("year")
        if financial_year == 0:
            financial_year = get_current_financial_year()
        archive_type = options.get("type")
        for arg in options[self.arg_name]:
            archive_type = arg

        if archive_type == "All":
            archive_all(financial_year)
            archive_cost_centre(financial_year)
            archive_treasury_l5(financial_year)
            self.stdout.write(
                self.style.SUCCESS("Archived full chart of account.")
            )
        else:
            row = ARCHIVE_TYPE[archive_type](financial_year)
            self.stdout.write(
                self.style.SUCCESS("Archived " + str(row) + " rows")
            )
