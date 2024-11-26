import factory
from faker import Faker

from costcentre.test.factories import CostCentreFactory
from chartofaccountDIT.test.factories import NaturalCodeFactory, ProgrammeCodeFactory
from gifthospitality.test.factories import GradeFactory
from payroll.models import (
    Employee,
    EmployeePayElement,
    PayElementTypeGroup,
    PayElementType,
)


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


class EmployeePayElementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeePayElement
