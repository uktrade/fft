import os
import pytest
from pathlib import Path  
from django.core.files import File

from chartofaccountDIT.test.factories import ProgrammeCodeFactory
from costcentre.test.factories import CostCentreFactory
from gifthospitality.test.factories import GradeFactory
from payroll.models import Employee

from ...services.ingest import import_payroll


TEST_DATA_DIR = Path(__file__).parent.parent / "test_assets" 

@pytest.fixture(autouse=True)
def setup(db):
    cost_centre_codes = ["888812", "888813", "888814"]
    programme_codes = ["338887", "338888", "338889"]
    grade_codes = [
        "SEO",
        "SCS",
        "HEO",
        "Grade 7",
        "Grade 6",
        "Faststream",
        "EO",
        "Contractor",
        "AO",
        "AA",
    ]
    [CostCentreFactory(cost_centre_code=id) for id in cost_centre_codes]
    [ProgrammeCodeFactory(programme_code=id) for id in programme_codes]
    [GradeFactory(grade=id) for id in grade_codes]
    yield


def test_ingest_payroll_success(db):
    """Testing valid records"""
    csv_file = TEST_DATA_DIR / "payroll_valid_records.csv"  
    with open(csv_file, "rb") as f:
        result = import_payroll(File(f))
        assert len(list(Employee.objects.all()))==15
        assert len(result.get("failed")) == 0
        assert result.get("error") is None
        assert result.get("created") == 15


def test_ingest_payroll_failed_record(db):
    """Testing failed records"""
    csv_file = TEST_DATA_DIR / "payroll_mixed_records.csv"
    with open(csv_file, "rb") as f:
        result = import_payroll(File(f))
        assert result.get("failed") is  not None
        print(result.get("failed"))
        print(result.get("created"))
        print(result.get("updated"))
        # assert len(list(Employee.objects.all()))==3



def test_ingest_payroll_error(db):
    """Testing mall structured  csv file"""
    csv_file = TEST_DATA_DIR / "payroll_error.csv"
    with open(csv_file, "rb") as f:
        try:
            result = import_payroll(File(f))
        except Exception as e:
            result = {  "error": str(e)}
        assert len(list(Employee.objects.all()))==0
        assert result.get("error") is not None


def test_ingest_payroll_update(db):
    """Testing update record functionality"""
    csv_file = TEST_DATA_DIR / "payroll_valid_records.csv"
    with open(csv_file, "rb") as f:
        result = import_payroll(File(f))
        result = import_payroll(File(f))
        assert len(result.get("failed")) == 0
        assert result.get("error") is None
        assert result.get("updated") == 15
        assert result.get("created") == 0
        assert len(list(Employee.objects.all()))==15

