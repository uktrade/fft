import factory
import factory.fuzzy
from faker import Faker

from chartofaccountDIT.test.factories import NaturalCodeFactory, ProgrammeCodeFactory
from core.models import Attrition, PayUplift
from core.test.factories import FinancialYearFactory
from costcentre.test.factories import CostCentreFactory
from gifthospitality.test.factories import GradeFactory
from payroll.models import Employee, EmployeePayPeriods, PayElementTypeGroup, Vacancy


fake = Faker()


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee
        django_get_or_create = ("employee_no",)

    cost_centre = factory.SubFactory(CostCentreFactory)
    programme_code = factory.SubFactory(ProgrammeCodeFactory)
    employee_no = factory.Sequence(lambda n: f"{n:08}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    grade = factory.SubFactory(GradeFactory)
    fte = 1.0
    assignment_status = "Active Assignment"


class EmployeePayPeriodsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeePayPeriods
        django_get_or_create = ("employee", "year")

    employee = factory.SubFactory(EmployeeFactory)
    year = factory.SubFactory(FinancialYearFactory)
    period_1 = True
    period_2 = True
    period_3 = True
    period_4 = True
    period_5 = True
    period_6 = True
    period_7 = True
    period_8 = True
    period_9 = True
    period_10 = True
    period_11 = True
    period_12 = True


class PayElementTypeGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PayElementTypeGroup
        django_get_or_create = ("name",)

    # name
    natural_code = factory.SubFactory(NaturalCodeFactory)


class VacancyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vacancy

    cost_centre = factory.SubFactory(CostCentreFactory)
    programme_code = factory.SubFactory(ProgrammeCodeFactory)
    grade = factory.SubFactory(GradeFactory)
    fte = 1.0

    recruitment_type = factory.fuzzy.FuzzyChoice(
        Vacancy.RecruitmentType.choices, getter=lambda c: c[0]
    )
    recruitment_stage = factory.fuzzy.FuzzyChoice(
        Vacancy.RecruitmentStage.choices, getter=lambda c: c[0]
    )
    appointee_name = factory.Faker("name")
    hiring_manager = factory.Faker("name")
    hr_ref = factory.Faker("name")


class PayModifierFactory(factory.django.DjangoModelFactory):
    financial_year = factory.SubFactory(FinancialYearFactory)
    apr = 0.0
    may = 0.0
    jun = 0.0
    jul = 0.0
    aug = 0.0
    sep = 0.0
    oct = 0.0
    nov = 0.0
    dec = 0.0
    jan = 0.0
    feb = 0.0
    mar = 0.0


class PayUpliftFactory(PayModifierFactory):
    class Meta:
        model = PayUplift


class AttritionFactory(PayModifierFactory):
    class Meta:
        model = Attrition

    cost_centre = factory.SubFactory(CostCentreFactory)
