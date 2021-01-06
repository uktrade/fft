from django.urls import path

from data_lake.views.forecast import ForecastViewSet

from data_lake.views.cost_centre_hierarchy import HierarchyViewSet
from data_lake.views.natural_code import NaturalCodeViewSet
from data_lake.views.programme_code import ProgrammeCodeViewSet
from data_lake.views.project_code import ProjectCodeViewSet
from data_lake.views.analysis1_code import Analysis1CodeViewSet
from data_lake.views.analysis2_code import Analysis2CodeViewSet
from data_lake.views.expenditure_category import ExpenditureCategoryViewSet

urlpatterns = [
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
