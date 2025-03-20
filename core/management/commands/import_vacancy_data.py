import csv

from django.core.management.base import BaseCommand

from payroll.models import Vacancy


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


# file_path = "core/management/commands/vacancies.csv"
# file_path = "core/management/commands/vacancy.csv"
class Command(BaseCommand):
    help = "Import Vacancy data"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, help="CSV file containing Vacancy data")

    def handle(self, *args, **options):
        file_path = options.get("file")
        self.stdout.write(self.style.SUCCESS("File received"))

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Index can probably be removed, used for testing
                # print("Year:", row["Year"])
                # print("January:", row["January"])
                # print("HRReason:", row["HRReason"])
                # print("Narrative:", row["Narrative"])
                # print("VacancyGrade:", row["VacancyGrade"])
                # print("CCCode:", row["CCCode"])
                # print("Programme:", row["Programme"])
                # print("Name:", row["Name"])
                # print("Hiring:", row["Hiring"])
                # print("HRStage:", row["HRStage"])
                # print("HRRef:", row["HRRef"])

                get_recruitment_stage(row["HRStage"])

                # vacancy = Vacancy.objects.get_or_create(
                #     cost_centre=row["CCCode"],
                #     programme_code=row["Programme"],
                #     grade=row["VacancyGrade"],
                #     recruitment_type=row["HRReason"],  # Check if this accesses correctly
                #     recruitment_stage=row["HRStage"],  # options 2,7 reworded, an integer
                #     appointee_name=row["Name"],
                #     hiring_manager=row["Hiring"],
                #     hr_ref=row["HRRef"],
                # )

                # pay_periods = VacancyPayPeriods.objects.get_or_create(
                #     vacancy=vacancy,
                #     year=get_boolean_period(row["Year"]),
                #     period_1=get_boolean_period(row["April"]),
                #     period_2=get_boolean_period(row["May"]),
                #     period_3=get_boolean_period(row["June"]),
                #     period_4=get_boolean_period(row["July"]),
                #     period_5=get_boolean_period(row["August"]),
                #     period_6=get_boolean_period(row["September"]),
                #     period_7=get_boolean_period(row["October"]),
                #     period_8=get_boolean_period(row["November"]),
                #     period_9=get_boolean_period(row["December"]),
                #     period_10=get_boolean_period(row["Janauary"]),
                #     period_11=get_boolean_period(row["February"]),
                #     period_12=get_boolean_period(row["March"]),
                # )


def get_boolean_period(period):
    return period == "1"


def get_recruitment_type(hr_reason):
    # Needs to match a value in RecruitmentType.choices
    pass


def get_recruitment_stage(hr_stage):
    # Needs to return an integer based on RecruitmentStages values
    # ADVERT and NOT_YET_ADVERTISED have been reworded and will need remapping
    if hr_stage:
        print(RECRUITMENT_STAGE_MAPPING[hr_stage])
    else:
        print("undefined")
