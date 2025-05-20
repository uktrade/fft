from pathlib import Path

import pytest
from django.core.files import File
from django.core.files.base import ContentFile

from chartofaccountDIT.test.factories import ProgrammeCodeFactory
from costcentre.test.factories import CostCentreFactory
from gifthospitality.test.factories import GradeFactory
from payroll.models import Employee

from ...services.ingest import import_payroll


TEST_DATA_DIR = Path(__file__).parent.parent / "test_assets"

CSV_FILE_HEADER = "employee_no,first_name,last_name,cost_centre_code,programme_code,grade,assignment_status,fte,basic_pay,ernic,pension"


def build_payroll_csv_file(rows):
    all_rows = "\n".join([CSV_FILE_HEADER, *rows])
    return ContentFile(all_rows.encode("utf-8"))


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
        result = import_payroll(File(f), payroll_period=1)
        assert len(list(Employee.objects.all())) == 20
        assert len(result.get("failed")) == 0
        assert result.get("created") == 20


def test_ingest_payroll_failed_record(db):
    """Testing failed records"""
    csv_file = TEST_DATA_DIR / "payroll_mixed_records.csv"
    with open(csv_file, "rb") as f:
        result = import_payroll(File(f), payroll_period=1)
        assert result.get("failed") is not None
        assert len(list(Employee.objects.all())) == 15


def test_ingest_payroll_error(db):
    """Testing mall structured csv file"""
    csv_file = TEST_DATA_DIR / "payroll_empty_rows.csv"
    with open(csv_file, "rb") as f:
        import_payroll(File(f), payroll_period=1)
        assert len(list(Employee.objects.all())) == 15


def test_ingest_payroll_update(db):
    """Testing update record functionality"""
    csv_file = TEST_DATA_DIR / "payroll_valid_records.csv"
    with open(csv_file, "rb") as f:
        result = import_payroll(File(f), payroll_period=1)
        result = import_payroll(File(f), payroll_period=1)
        assert len(result.get("failed")) == 0
        assert result.get("updated") == 20
        assert result.get("created") == 0
        assert len(list(Employee.objects.all())) == 20


def test_payroll_pay_periods(db):
    rows = ["150892,Jack,Wright,888813,338888,SCS,Loan Out - Non Payroll,1,1500,0,0"]
    import_payroll(build_payroll_csv_file(rows), payroll_period=1)
    emp = Employee.objects.get(employee_no="150892")
    assert emp.pay_periods.first().periods == [True] * 12


def test_non_payroll_pay_periods(db):
    rows = ["150892,Jack,Wright,888813,338888,SCS,Loan Out - Non Payroll,0,0,0,0"]
    import_payroll(build_payroll_csv_file(rows), payroll_period=1)
    emp = Employee.objects.get(employee_no="150892")
    assert emp.pay_periods.first().periods == [False] * 12


def test_employee_joins(db):
    rows = ["150892,Jack,Wright,888813,338888,Grade 7,Active Assignment,1,3000,150,200"]
    import_payroll(build_payroll_csv_file(rows), payroll_period=2)
    emp = Employee.objects.get(employee_no="150892")
    assert emp.pay_periods.first().periods == [False] + ([True] * 11)


def test_employee_leaves(db):
    rows = ["150892,Jack,Wright,888813,338888,Grade 7,Active Assignment,1,3000,150,200"]
    import_payroll(build_payroll_csv_file(rows), payroll_period=2)
    import_payroll(build_payroll_csv_file([]), payroll_period=3)
    emp = Employee.objects.get(employee_no="150892")

    assert emp.has_left
    assert emp.pay_periods.first().periods == [False, True] + ([False] * 10)


def test_employee_rejoins(db):
    rows = ["150892,Jack,Wright,888813,338888,Grade 7,Active Assignment,1,3000,150,200"]
    import_payroll(build_payroll_csv_file(rows), payroll_period=2)
    import_payroll(build_payroll_csv_file([]), payroll_period=3)
    import_payroll(build_payroll_csv_file(rows), payroll_period=4)
    emp = Employee.objects.get(employee_no="150892")

    assert not emp.has_left
    assert emp.pay_periods.first().periods == [False, True, False] + ([True] * 9)
