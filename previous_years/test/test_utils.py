from django.contrib.auth.models import Permission
from django.test import TestCase

from chartofaccountDIT.test.factories import (
    HistoricalAnalysis1Factory,
    HistoricalAnalysis2Factory,
    HistoricalExpenditureCategoryFactory,
    HistoricalNaturalCodeFactory,
    HistoricalProgrammeCodeFactory,
    HistoricalProjectCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import ArchivedCostCentreFactory

from previous_years.models import (
    ArchivedFinancialCode,
    ArchivedForecastData,
)


class DownloadPastYearForecastSetup(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)
        # 2019 is created when the database is created, so it exists
        self.archived_year = 2019
        archived_year_obj = FinancialYear.objects.filter(
            financial_year=self.archived_year
        ).first()
        # Just in case 2019 does not exist
        assert archived_year_obj is not None
        self.cost_centre_code = "109189"
        self.cost_centre_name = "Test cost centre"
        self.group_code = "1090TT"
        self.group_name = "Test group name"
        self.directorate_code = "10900T"
        self.directorate_name = "Test directorate name"
        self.natural_account_code = 52191003
        self.natural_account_description = "Test nac description"
        self.programme_code = "310940"
        self.programme_description = "Test programme description"
        self.project_code = "0123"
        self.project_description = "Test project description"
        self.analisys1 = "00798"
        self.analisys2 = "00321"
        cc_obj = ArchivedCostCentreFactory.create(
            cost_centre_code=self.cost_centre_code,
            cost_centre_name=self.cost_centre_name,
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group_code=self.group_code,
            group_name=self.group_name,
            financial_year=archived_year_obj,
        )
        project_obj = HistoricalProjectCodeFactory.create(
            project_code=self.project_code,
            financial_year=archived_year_obj,
            project_description=self.project_description,
        )
        self.budget_type_id = "AME"
        programme_obj = HistoricalProgrammeCodeFactory.create(
            programme_code=self.programme_code,
            programme_description=self.programme_description,
            budget_type_id=self.budget_type_id,
            financial_year=archived_year_obj,
        )

        expenditure_category_obj = HistoricalExpenditureCategoryFactory.create(
            financial_year=archived_year_obj
        )
        self.expenditure_category_id = expenditure_category_obj.id
        nac_obj = HistoricalNaturalCodeFactory.create(
            natural_account_code=self.natural_account_code,
            natural_account_code_description=self.natural_account_description,
            economic_budget_code="CAPITAL",
            expenditure_category=expenditure_category_obj,
            financial_year=archived_year_obj,
        )

        analysis2_obj = HistoricalAnalysis2Factory.create(
            analysis2_code=self.analisys2, financial_year=archived_year_obj
        )
        analysis1_obj = HistoricalAnalysis1Factory.create(
            analysis1_code=self.analisys1, financial_year=archived_year_obj
        )
        financial_code_obj = ArchivedFinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cc_obj,
            natural_account_code=nac_obj,
            analysis1_code=analysis1_obj,
            analysis2_code=analysis2_obj,
            project_code=project_obj,
            financial_year=archived_year_obj,
        )

        self.expenditure_type_name = financial_code_obj.forecast_expenditure_type
        self.forecast_expenditure_type_id = (
            financial_code_obj.forecast_expenditure_type.forecast_expenditure_type_name
        )

        previous_year_obj = ArchivedForecastData.objects.create(
            financial_year=archived_year_obj, financial_code=financial_code_obj,
        )
        self.outturn = {
            "budget": 1234500,
            "apr": 1200000,
            "may": 3412000,
            "jun": 9876000,
            "jul": 5468970,
            "aug": 3421900,
            "sep": 6901110,
            "oct": 7622200,
            "nov": 6955501,
            "dec": 8434422,
            "jan": 5264091,
            "feb": 4521111,
            "mar": 9090111,
            "adj01": 5464644,
            "adj02": -2118976,
            "adj03": 3135450,
        }
        self.budget = self.outturn["budget"]
        self.year_total = sum(self.outturn.values()) - self.budget
        self.underspend_total = self.budget - self.year_total
        self.spend_to_date_total = self.year_total

        previous_year_obj.budget = self.outturn["budget"] * 100
        previous_year_obj.apr = self.outturn["apr"] * 100
        previous_year_obj.may = self.outturn["may"] * 100
        previous_year_obj.jun = self.outturn["jun"] * 100
        previous_year_obj.jul = self.outturn["jul"] * 100
        previous_year_obj.aug = self.outturn["aug"] * 100
        previous_year_obj.sep = self.outturn["sep"] * 100
        previous_year_obj.oct = self.outturn["oct"] * 100
        previous_year_obj.nov = self.outturn["nov"] * 100
        previous_year_obj.dec = self.outturn["dec"] * 100
        previous_year_obj.jan = self.outturn["jan"] * 100
        previous_year_obj.feb = self.outturn["feb"] * 100
        previous_year_obj.mar = self.outturn["mar"] * 100
        previous_year_obj.adj1 = self.outturn["adj01"] * 100
        previous_year_obj.adj2 = self.outturn["adj02"] * 100
        previous_year_obj.adj3 = self.outturn["adj03"] * 100
        previous_year_obj.save()
        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()
