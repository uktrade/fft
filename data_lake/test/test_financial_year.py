from core.models import FinancialYear
from data_lake.test.utils import DataLakeTesting


class Analysis1CodeTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        financial_year_queryset = FinancialYear.objects.all().order_by("financial_year")
        self.current_code = financial_year_queryset[0].financial_year
        self.archived_code = financial_year_queryset[1].financial_year

        self.url_name = "data_lake_financial_year"
        self.row_lenght = 4
        self.code_position = 0
        self.check_data()
