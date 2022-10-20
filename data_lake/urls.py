from django.urls import path

from data_lake.views.actual import ActualViewSet
from data_lake.views.actual_split import ActualSplitViewSet
from data_lake.views.analysis1_code import Analysis1CodeViewSet
from data_lake.views.analysis2_code import Analysis2CodeViewSet
from data_lake.views.budget import BudgetViewSet
from data_lake.views.budget_profiled_actual import BudgetActualViewSet
from data_lake.views.budget_profiled_forecast import BudgetForecastViewSet
from data_lake.views.commercial_category import CommercialCategoryViewSet
from data_lake.views.cost_centre_hierarchy import HierarchyViewSet
from data_lake.views.expenditure_category import ExpenditureCategoryViewSet
from data_lake.views.fco_mapping import FCOMappingViewSet
from data_lake.views.financial_year import FinancialYearViewSet
from data_lake.views.forecast import ForecastViewSet
from data_lake.views.inter_entity import InterEntityViewSet
from data_lake.views.natural_code import NaturalCodeViewSet
from data_lake.views.programme_code import ProgrammeCodeViewSet
from data_lake.views.project_code import ProjectCodeViewSet


urlpatterns = [
    path(
        "budget_forecast/",
        BudgetForecastViewSet.as_view({"get": "list"}),
        name="data_lake_budget_forecast",
    ),
    path(
        "budget_actual/",
        BudgetActualViewSet.as_view({"get": "list"}),
        name="data_lake_budget_actual",
    ),
    path(
        "actual_split/",
        ActualSplitViewSet.as_view({"get": "list"}),
        name="data_lake_actual_split",
    ),
    path(
        "financialyear/",
        FinancialYearViewSet.as_view({"get": "list"}),
        name="data_lake_financial_year",
    ),
    path(
        "actual/",
        ActualViewSet.as_view({"get": "list"}),
        name="data_lake_actual",
    ),
    path(
        "budget/",
        BudgetViewSet.as_view({"get": "list"}),
        name="data_lake_budget",
    ),
    path(
        "interentity/",
        InterEntityViewSet.as_view({"get": "list"}),
        name="data_lake_inter_entity",
    ),
    path(
        "fcomapping/",
        FCOMappingViewSet.as_view({"get": "list"}),
        name="data_lake_fco_mapping",
    ),
    path(
        "commercialcategory/",
        CommercialCategoryViewSet.as_view({"get": "list"}),
        name="data_lake_commercial_category",
    ),
    path(
        "forecast/",
        ForecastViewSet.as_view({"get": "list"}),
        name="data_lake_forecast",
    ),
    path(
        "hierarchy/",
        HierarchyViewSet.as_view({"get": "list"}),
        name="data_lake_hierachy",
    ),
    path(
        "naturalcode/",
        NaturalCodeViewSet.as_view({"get": "list"}),
        name="data_lake_natural_code",
    ),
    path(
        "programmecode/",
        ProgrammeCodeViewSet.as_view({"get": "list"}),
        name="data_lake_programme_code",
    ),
    path(
        "projectcode/",
        ProjectCodeViewSet.as_view({"get": "list"}),
        name="data_lake_project_code",
    ),
    path(
        "analysis1code/",
        Analysis1CodeViewSet.as_view({"get": "list"}),
        name="data_lake_analysis1_code",
    ),
    path(
        "analysis2code/",
        Analysis2CodeViewSet.as_view({"get": "list"}),
        name="data_lake_analysis2_code",
    ),
    path(
        "expenditurecategory/",
        ExpenditureCategoryViewSet.as_view({"get": "list"}),
        name="data_lake_expenditure_category",
    ),
]
