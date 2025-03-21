import csv

from django.core.management.base import BaseCommand

from chartofaccountDIT.models import ProgrammeCode
from core.models import FinancialYear
from costcentre.models import CostCentre
from gifthospitality.models import Grade
from payroll.models import Vacancy, VacancyPayPeriods


RECRUITMENT_STAGE_MAPPING = {
    "Preparing": Vacancy.RecruitmentStage.PREPARING,
    "Advert (Vac ref to be provided)": Vacancy.RecruitmentStage.ADVERT,
    "Sift": Vacancy.RecruitmentStage.SIFT,
    "Interview": Vacancy.RecruitmentStage.INTERVIEW,
    "Onboarding": Vacancy.RecruitmentStage.ONBOARDING,
    "Unsuccessful recruitment": Vacancy.RecruitmentStage.UNSUCCESSFUL_RECRUITMENT,
    "Not (yet) advertised": Vacancy.RecruitmentStage.NOT_YET_ADVERTISED,
    "Not Required": Vacancy.RecruitmentStage.NOT_REQUIRED,
}

RECRUITMENT_TYPE_MAPPING = {
    "Expression of Interest": Vacancy.RecruitmentType.EXPRESSION_OF_INTEREST,
    "External Recruitment (Non-bulk)": Vacancy.RecruitmentType.EXTERNAL_RECRUITMENT_NON_BULK,
    "External Recruitment (Bulk campaign)": Vacancy.RecruitmentType.EXTERNAL_RECRUITMENT_BULK,
    "Internal Managed Move": Vacancy.RecruitmentType.INTERNAL_MANAGED_MOVE,
    "Internal Redeployment": Vacancy.RecruitmentType.INTERNAL_REDEPLOYMENT,
    "Other": Vacancy.RecruitmentType.OTHER,
    "Inactive Post": Vacancy.RecruitmentType.INACTIVE_POST,
    "Expected Unknown Leavers": Vacancy.RecruitmentType.EXPECTED_UNKNOWN_LEAVERS,
    "Missing Staff": Vacancy.RecruitmentType.MISSING_STAFF,
}


# file_path = "core/management/commands/vacancies.csv"
# file_path = "core/management/commands/vacancy.csv"
class Command(BaseCommand):
    help = "Import Vacancy data"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, help="CSV file containing Vacancy data")
        # Either file or s3_file, use boto3
        # fft-main-dev

    def handle(self, *args, **options):
        file_path = options.get("file")
        self.stdout.write(self.style.SUCCESS("File received"))

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cost_centre = CostCentre.objects.get(cost_centre_code=row["CCCode"])
                programme_code = ProgrammeCode.objects.get(
                    programme_code=row["Programme"]
                )
                grade = Grade.objects.get(grade=row["VacancyGrade"])

                vacancy, created = Vacancy.objects.get_or_create(
                    cost_centre=cost_centre,
                    programme_code=programme_code,
                    grade=grade,
                    recruitment_type=get_recruitment_type(row["HRReason"]),
                    recruitment_stage=get_recruitment_stage(row["HRStage"]),
                    appointee_name=handle_empty_value(row["Name"]),
                    hiring_manager=handle_empty_value(row["Hiring"]),
                    hr_ref=handle_empty_value(row["HRRef"]),
                )

                if not created:
                    self.stdout.write(self.style.WARNING("Vacancy already exists"))
                else:
                    financial_year = FinancialYear.objects.get(
                        financial_year=row["Year"]
                    )

                    VacancyPayPeriods.objects.get_or_create(
                        vacancy=vacancy,
                        year=financial_year,
                        period_1=get_boolean_period(row["April"]),
                        period_2=get_boolean_period(row["May"]),
                        period_3=get_boolean_period(row["June"]),
                        period_4=get_boolean_period(row["July"]),
                        period_5=get_boolean_period(row["August"]),
                        period_6=get_boolean_period(row["September"]),
                        period_7=get_boolean_period(row["October"]),
                        period_8=get_boolean_period(row["November"]),
                        period_9=get_boolean_period(row["December"]),
                        period_10=get_boolean_period(row["January"]),
                        period_11=get_boolean_period(row["February"]),
                        period_12=get_boolean_period(row["March"]),
                        notes=row["Narrative"],
                    )

                    self.stdout.write(self.style.SUCCESS("Vacancy created"))


def get_boolean_period(period):
    return period == "1"


def handle_empty_value(value):
    return value if value else None


def get_recruitment_type(hr_reason):
    if hr_reason:
        return RECRUITMENT_TYPE_MAPPING[hr_reason]
    else:
        return Vacancy.RecruitmentType.EXPRESSION_OF_INTEREST


def get_recruitment_stage(hr_stage):
    if hr_stage:
        return RECRUITMENT_STAGE_MAPPING[hr_stage]
    else:
        return Vacancy.RecruitmentStage.PREPARING
