import io

from django.test import (
    RequestFactory,
    TestCase,
)

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import (
    CostCentreFactory,
    DirectorateFactory,
)

from forecast.import_csv import import_adi_file
from forecast.models import (
    FinancialCode,
    ForecastMonthlyFigure,
)


class ImportBudgetsTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        self.test_year = 2019
        self.test_period = 9
        self.factory = RequestFactory()
        self.cost_centre_code = "109189"
        self.natural_account_code = 52191003
        self.programme_code = "310940"
        self.project_code = "0123"
        self.analisys1 = "00798"
        self.analisys2 = "00321"
        self.test_amount = 100
        self.directorate_obj = DirectorateFactory.create(directorate_code="T123")
        CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code, directorate=self.directorate_obj
        )
        NaturalCodeFactory.create(
            natural_account_code=self.natural_account_code,
            economic_budget_code="CAPITAL",
        )
        ProgrammeCodeFactory.create(programme_code=self.programme_code)
        ProjectCodeFactory.create(project_code=self.project_code)
        Analysis1Factory.create(analysis1_code=self.analisys1)
        Analysis2Factory.create(analysis2_code=self.analisys2)
        self.year_obj = FinancialYear.objects.get(financial_year=2019)
        self.year_obj.current = True
        self.year_obj.save

    def get_csv_data(self):
        header = "Entity,Cost Centre,Natural Account,Programme,Analysis,Analysis2," \
                 "Project,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC,JAN,FEB,MAR," \
                 "ADJ01,ADJ02,ADJ03"
        line1 = f"3000,{self.cost_centre_code},{self.natural_account_code}," \
                f"{self.programme_code},{self.analisys1},{self.analisys2}," \
                f"{self.project_code}," \
                f"0,200,300,400,500,600,700,800,900,1000,1100,1200,0,0,0"
        return io.StringIO(f"{header}\n{line1}\n")

    def test_upload_budget_report(self):
        result = import_adi_file(self.get_csv_data())
        self.assert_(result, True)
        self.assertEqual(
            ForecastMonthlyFigure.objects.all().count(), 11,
        )
        self.assertEqual(FinancialCode.objects.all().count(), 1)
        financial_code_obj = FinancialCode.objects.all().first()
        self.assertEqual(financial_code_obj.cost_centre_id, self.cost_centre_code)
        self.assertEqual(financial_code_obj.analysis1_code_id, self.analisys1)
        self.assertEqual(financial_code_obj.analysis2_code_id, self.analisys2)
        self.assertEqual(financial_code_obj.project_code_id, self.project_code)
        self.assertEqual(financial_code_obj.programme_id, self.programme_code)
        self.assertEqual(
            financial_code_obj.natural_account_code_id, self.natural_account_code
        )
