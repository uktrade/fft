from django.core.management.base import BaseCommand

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    BudgetType,
    ExpenditureCategory,
    NACCategory,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)

import core

from costcentre.models import (
    CostCentre,
    DepartmentalGroup,
    Directorate,
)

from forecast.models import (
    FinancialCode,
    ForecastMonthlyFigure,
)


class CostHierarchy:
    name = "Cost Centre Hierarchy"
    counter = 0

    def create_departmental_group(
        self, group_code, howmany_directorate, howmany_cost_centres
    ):
        departmental_group = DepartmentalGroup.objects.create(
            group_code=group_code,
            active=True,
            group_name="Departmental Group {}".format(self.counter),
        )
        self.counter += 1
        directorate_code_base = int(group_code[0:4]) * 10
        for i in range(howmany_directorate):
            self.create_directorate(
                departmental_group,
                "{}A".format(directorate_code_base),
                howmany_cost_centres,
            )
            directorate_code_base += 1

    def create_directorate(
        self, departmental_group, directorate_code, howmany_cost_centres
    ):
        directorate = Directorate.objects.create(
            directorate_code=directorate_code,
            active=True,
            directorate_name="Directorate {}".format(self.counter),
            group=departmental_group,
        )
        self.counter += 1
        for i in range(howmany_cost_centres):
            CostCentre.objects.create(
                cost_centre_code=888810 + self.counter,
                active=True,
                cost_centre_name="Cost Centre {}".format(self.counter),
                directorate=directorate,
            )
            self.counter += 1

    def clear(self):
        ForecastMonthlyFigure.objects.all().delete()
        FinancialCode.objects.all().delete()
        CostCentre.objects.all().delete()
        Directorate.objects.all().delete()
        DepartmentalGroup.objects.all().delete()

    def create(self):
        """Clear the Cost Centre, Directorate
        and Group tables, and create the stub data"""
        self.clear()
        self.create_departmental_group("8888AA", 1, 1)
        # self.create_departmental_group('8123AA', 5, 3)
        # self.create_departmental_group('8213CC', 5, 3)
        # self.create_departmental_group('8456AA', 5, 3)


class ProgrammeCodes:
    name = "Programme Codes"

    def clear(self):
        ForecastMonthlyFigure.objects.all().delete()
        ProgrammeCode.objects.all().delete()

    def create(self):
        self.clear()
        budget_type_code = "AME"
        budget_type = BudgetType.objects.get(pk=budget_type_code)
        ProgrammeCode.objects.create(
            programme_code='338888',
            programme_description='Programme {}'.format(budget_type_code),
            active=True,
            budget_type_fk=budget_type,
        )
        budget_type_code = "DEL"
        budget_type = BudgetType.objects.get(pk=budget_type_code)
        ProgrammeCode.objects.create(
            programme_code='338889',
            programme_description='Programme {}'.format(budget_type_code),
            active=True,
            budget_type_fk=budget_type,
        )
        budget_type_code = "ADMIN"
        budget_type = BudgetType.objects.get(pk=budget_type_code)
        ProgrammeCode.objects.create(
            programme_code='338887',
            programme_description='Admin DEL',
            active=True,
            budget_type_fk=budget_type,
        )


class Analysis1Codes:
    name = "Analysis 1 Codes"

    def clear(self):
        ForecastMonthlyFigure.objects.all().delete()
        Analysis1.objects.all().delete()

    def create(self):
        self.clear()
        Analysis1.objects.create(
            active=True, analysis1_code="10001",
            analysis1_description="Analysis 1 - 0",
        )
        Analysis1.objects.create(
            active=True, analysis1_code="10002",
            analysis1_description="Analysis 1 - 1",
        )
        Analysis1.objects.create(
            active=True, analysis1_code="10004",
            analysis1_description="Analysis 1 - 2",
        )
        Analysis1.objects.create(
            active=True, analysis1_code="10005",
            analysis1_description="Analysis 1 - 3",
        )
        Analysis1.objects.create(
            active=True, analysis1_code="10006",
            analysis1_description="Analysis 1 - 4",
        )


class Analysis2Codes:
    name = "Analysis 2 codes"

    def clear(self):
        ForecastMonthlyFigure.objects.all().delete()
        Analysis2.objects.all().delete()

    def create(self):
        self.clear()
        Analysis2.objects.create(
            active=True, analysis2_code="40001",
            analysis2_description="Analysis 2 - 0",
        )
        Analysis2.objects.create(
            active=True, analysis2_code="40002",
            analysis2_description="Analysis 2 - 1",
        )
        Analysis2.objects.create(
            active=True, analysis2_code="40004",
            analysis2_description="Analysis 2 - 2",
        )
        Analysis2.objects.create(
            active=True, analysis2_code="40005",
            analysis2_description="Analysis 2 - 3",
        )
        Analysis2.objects.create(
            active=True, analysis2_code="40006",
            analysis2_description="Analysis 2 - 4",
        )


class ProjectCodes:
    name = "Project codes"

    def clear(self):
        ForecastMonthlyFigure.objects.all().delete()
        ProjectCode.objects.all().delete()

    def create(self):
        self.clear()
        ProjectCode.objects.create(
            active=True, project_code=5000,
            project_description="Project 1",
        )
        ProjectCode.objects.create(
            active=True, project_code=5001,
            project_description="Project 2",
        )
        ProjectCode.objects.create(
            active=True, project_code=5002,
            project_description="Project 3",
        )
        ProjectCode.objects.create(
            active=True, project_code=5003,
            project_description="Project 4",
        )
        ProjectCode.objects.create(
            active=True, project_code=5004,
            project_description="Project 5",
        )


# TODO rename model NaturalCode to NaturalAccountCode
# TODO check CASCADE in model
class NaturalAccountCodes:
    name = "Natural Account Codes"

    def clear(self):
        ForecastMonthlyFigure.objects.all().delete()
        # clear the NAC budget field in
        # expenditure codes before clearing
        # the natural account codes
        q = ExpenditureCategory.objects.all()
        for q1 in q:
            q1.linked_budget_code = None
            q1.save()
        NaturalCode.objects.all().delete()
        ExpenditureCategory.objects.all().delete()
        NACCategory.objects.all().delete()

    def create_natural_account_code_expenditure_group(
        self, nac_category, economic_budget_code, cat_description, nac_base, howmany
    ):
        expenditure_category = ExpenditureCategory.objects.create(
            active=True,
            grouping_description=cat_description,
            description="Expenditure: {}".format(cat_description),
            further_description="",
            NAC_category=nac_category,
        )
        natural_account_code = NaturalCode.objects.create(
            active=True,
            natural_account_code=nac_base,
            natural_account_code_description="NAC  {} - budget".format(
                cat_description
            ),
            used_for_budget=True,
            economic_budget_code=economic_budget_code,
            expenditure_category=expenditure_category,
        )
        expenditure_category.linked_budget_code = natural_account_code
        expenditure_category.save()
        for x in range(howmany):
            nac_base += 1
            NaturalCode.objects.create(
                active=True,
                natural_account_code=nac_base,
                natural_account_code_description="NAC {} {}".format(
                    cat_description,
                    x,
                ),
                used_for_budget=False,
                economic_budget_code=economic_budget_code,
                expenditure_category=expenditure_category,
            )

    def create(self):
        self.clear()
        # use real values for NAC categories. Easier than inventing some
        nac_category = NACCategory.objects.create(
            active=True, NAC_category_description="Pay"
        )
        self.create_natural_account_code_expenditure_group(
            nac_category,
            "RESOURCE",
            "Contractors (Pay)",
            71111000,
            5,
        )

        nac_category = NACCategory.objects.create(
            active=True,
            NAC_category_description="NonCash",
        )
        self.create_natural_account_code_expenditure_group(
            nac_category,
            "RESOURCE",
            "Provisions",
            71112000,
            2,
        )

        nac_category = NACCategory.objects.create(
            active=True, NAC_category_description="NonPay"
        )
        self.create_natural_account_code_expenditure_group(
            nac_category,
            "RESOURCE",
            "Staff Welfare",
            71113000,
            2,
        )
        self.create_natural_account_code_expenditure_group(
            nac_category,
            "RESOURCE",
            "Estates",
            71114000,
            1,
        )
        self.create_natural_account_code_expenditure_group(
            nac_category,
            "RESOURCE",
            "Grant",
            71115000,
            4,
        )

        nac_category = NACCategory.objects.create(
            active=True, NAC_category_description="Capital"
        )
        self.create_natural_account_code_expenditure_group(
            nac_category,
            "CAPITAL",
            "Estates (Capital)",
            71121000,
            4,
        )


class Command(BaseCommand):
    TEST_TYPE = {
        "CostCentre": CostHierarchy,
        "Programme": ProgrammeCodes,
        "NAC": NaturalAccountCodes,
        "Analysis1": Analysis1Codes,
        "Analysis2": Analysis2Codes,
        "Project": ProjectCodes,
    }

    help = "Create stub data. Allowed types are - All - {}".format(
        " - ".join(TEST_TYPE.keys())
    )
    arg_name = "what"

    def add_arguments(self, parser):
        # Positional arguments, default to All for no argument
        parser.add_argument(self.arg_name, nargs="*", default=["All"])

        # Named (optional) arguments
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete stub data instead of creating it",
        )

    def create(self, what):
        # The modified save writes the current user to the log, but
        # the user is not available while we are running a command.
        # So set  the test flag to stop writing to the log
        core._called_from_test = True
        p = what()
        p.create()
        del core._called_from_test
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully completed stub data creation for {}.".format(
                    p.name
                )
            )
        )

    def clear(self, what):
        core._called_from_test = True
        p = what()
        p.clear()
        del core._called_from_test
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully cleared stub data for {}.".format(
                    p.name
                )
            )
        )

    def handle(self, *args, **options):
        if options["delete"]:
            func = self.clear
        else:
            func = self.create
        for arg in options[self.arg_name]:
            if arg == "All":
                for t in self.TEST_TYPE.values():
                    func(t)
                return
            else:
                func(self.TEST_TYPE[arg])
