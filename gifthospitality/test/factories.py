import factory
from django.utils import timezone

from costcentre.test.factories import DepartmentalGroupFactory
from gifthospitality.models import (
    GiftAndHospitality,
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
    Grade,
)


class GradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grade
        django_get_or_create = ("grade",)

    grade = factory.Sequence(lambda n: f"Grade {n}")
    gradedescription = factory.Sequence(lambda n: f"Description of Grade {n}")


class GiftsAndHospitalityCategoryFactory(factory.django.DjangoModelFactory):
    """
    Define GiftsAndHospitalityCategory Factory
    """

    class Meta:
        model = GiftAndHospitalityCategory

    gif_hospitality_category = "Event"
    sequence_no = 1


class GiftsAndHospitalityClassificationFactory(factory.django.DjangoModelFactory):
    """
    Define CostCentre Factory
    """

    class Meta:
        model = GiftAndHospitalityClassification

    gift_type = "Hospitality"
    gif_hospitality_classification = "Meal"
    sequence_no = 1


class GiftsAndHospitalityCompanyFactory(factory.django.DjangoModelFactory):
    """
    Define CostCentre Factory
    """

    class Meta:
        model = GiftAndHospitalityCompany

    gif_hospitality_company = "Large Company 1"
    sequence_no = 1


class GiftsAndHospitalityFactory(factory.django.DjangoModelFactory):
    """
    Define GiftsAndHospitality Factory
    """

    class Meta:
        model = GiftAndHospitality

    classification = factory.SubFactory(GiftsAndHospitalityClassificationFactory)
    group_name = "Group 1"
    date_agreed = factory.LazyFunction(lambda: timezone.now().date())
    venue = "Large Venue"
    reason = "Meal at event for speaking."
    value = 99
    rep = "John Doe"
    group = factory.SubFactory(DepartmentalGroupFactory)
    offer = "Offered"
    company_rep = "Jane Doe"
    company = factory.SubFactory(GiftsAndHospitalityCompanyFactory)
    company_name = ""
    action_taken = "Action1"
    entered_by = "John Doe"
    entered_date_stamp = factory.LazyFunction(lambda: timezone.now().date())
    category = factory.SubFactory(GiftsAndHospitalityCategoryFactory)
    grade = factory.SubFactory(GradeFactory)
