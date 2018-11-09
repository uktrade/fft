import pytest

from .factories import GiftsAndHospitalityCategoryFactory, \
    GiftsAndHospitalityClassificationFactory, \
    GiftsAndHospitalityCompanyFactory, \
    GiftsAndHospitalityFactory


# https://medium.com/@dwernychukjosh/testing-models-with-django-using-pytest-and-factory-boy-a2985adce7b3

@pytest.mark.django_db
def test_GiftsAndHospitalityCompany_model():
    model_test = GiftsAndHospitalityCompanyFactory(company='Test1')
    assert model_test.company == 'Test1'


@pytest.mark.django_db
def test_GiftsAndHospitalityClassification_model():
    model_test = GiftsAndHospitalityClassificationFactory(classification='Test1',
                                                          gift_type = 'Test2')
    assert model_test.classification == 'Test1'
    assert model_test.gift_type == 'Test2'
