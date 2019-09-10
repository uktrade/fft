import pytest

from .factories import GiftsAndHospitalityClassificationFactory, \
    GiftsAndHospitalityCompanyFactory


# https://medium.com/@dwernychukjosh/testing-models-with-django-using-pytest-and-factory-boy-a2985adce7b3

@pytest.mark.django_db
def test_GiftsAndHospitalityCompany_model():
    model_test = GiftsAndHospitalityCompanyFactory(gif_hospitality_company='Test1')
    assert model_test.gif_hospitality_company == 'Test1'


@pytest.mark.django_db
def test_GiftsAndHospitalityClassification_model():
    model_test = GiftsAndHospitalityClassificationFactory(gif_hospitality_classification='Test1',
                                                          gift_type='Test2')
    assert model_test.gif_hospitality_classification == 'Test1'
    assert model_test.gift_type == 'Test2'

