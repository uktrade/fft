import factory

from gifthospitality.models import (
    GiftAndHospitality,
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
    Grade,
)


class GiftsAndHospitalityFactory(factory.django.DjangoModelFactory):
    """
    Define GiftsAndHospitality Factory
    """

    class Meta:
        model = GiftAndHospitality


class GiftsAndHospitalityCategoryFactory(factory.django.DjangoModelFactory):
    """
    Define GiftsAndHospitalityCategory Factory
    """

    class Meta:
        model = GiftAndHospitalityCategory


class GiftsAndHospitalityClassificationFactory(factory.django.DjangoModelFactory):
    """
    Define CostCentre Factory
    """

    class Meta:
        model = GiftAndHospitalityClassification


class GiftsAndHospitalityCompanyFactory(factory.django.DjangoModelFactory):
    """
    Define CostCentre Factory
    """

    class Meta:
        model = GiftAndHospitalityCompany


class GradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grade
        django_get_or_create = ("grade",)

    grade = factory.Sequence(lambda n: f"Grade {n}")
    gradedescription = factory.Sequence(lambda n: f"Description of Grade {n}")
