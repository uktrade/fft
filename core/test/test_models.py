from core.models import FinancialYear

import pytest

from .factories import FinancialYearFactory


# https://medium.com/@dwernychukjosh/testing-models-with-django-using-pytest-and-factory-boy-a2985adce7b3

@pytest.mark.django_db
def test_FinancialYear_model():
    model_test = FinancialYearFactory(financial_year=2018)
    assert model_test.financial_year == 2018

