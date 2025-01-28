import factory
import factory.fuzzy
from faker import Faker

from chartofaccountDIT.test.factories import NaturalCodeFactory, ProgrammeCodeFactory
from core.models import Attrition, PayUplift
from core.test.factories import FinancialYearFactory
from costcentre.test.factories import CostCentreFactory
from gifthospitality.test.factories import GradeFactory
from payroll.models import Employee, PayElementType, PayElementTypeGroup, Vacancy


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


class PayElementTypeGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PayElementTypeGroup
        django_get_or_create = ("name",)

    # name
    natural_code = factory.SubFactory(NaturalCodeFactory)


class PayElementTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PayElementType
        django_get_or_create = ("name",)

    # name
    natural_code = factory.SubFactory(NaturalCodeFactory)
    group = factory.SubFactory(PayElementTypeGroupFactory)


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


class PayUpliftFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PayUplift

    financial_year = factory.SubFactory(FinancialYearFactory)
    apr = 1.0
    may = 1.0
    jun = 1.0
    jul = 1.0
    aug = 1.0
    sep = 1.0
    oct = 1.0
    nov = 1.0
    dec = 1.0
    jan = 1.0
    feb = 1.0
    mar = 1.0


class AttritionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attrition

    cost_centre = factory.SubFactory(CostCentreFactory)
    financial_year = factory.SubFactory(FinancialYearFactory)
    apr = 1.0
    may = 1.0
    jun = 1.0
    jul = 1.0
    aug = 1.0
    sep = 1.0
    oct = 1.0
    nov = 1.0
    dec = 1.0
    jan = 1.0
    feb = 1.0
    mar = 1.0
