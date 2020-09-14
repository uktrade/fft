from django.urls import path, register_converter

from chartofaccountDIT.views import (
    FilteredAnalysis1ListView,
    FilteredAnalysis2ListView,
    FilteredCommercialCategoryListView,
    FilteredExpenditureCategoryListView,
    FilteredFCOMappingView,
    FilteredInterEntityView,
    FilteredNACListView,
    FilteredProgrammeView,
    FilteredProjectView,
    HistoricalFilteredAnalysis1ListView,
    HistoricalFilteredAnalysis2ListView,
    HistoricalFilteredCommercialCategoryListView,
    HistoricalFilteredExpenditureCategoryListView,
    HistoricalFilteredFCOMappingView,
    HistoricalFilteredInterEntityView,
    HistoricalFilteredNACListView,
    HistoricalFilteredProgrammeView,
    HistoricalFilteredProjectView,
    choose_year,
    quick_links,
)

from core.utils.generic_helpers import GetValidYear


register_converter(GetValidYear, 'yyyy')


urlpatterns = [
    path("naturalcode/", FilteredNACListView.as_view(), name="natural_code"),
    path(
        "financecategory/",
        FilteredExpenditureCategoryListView.as_view(),
        name="finance_category",
    ),
    path(
        "commercialcategory/",
        FilteredCommercialCategoryListView.as_view(),
        name="commercial_category",
    ),
    path("analysis1/", FilteredAnalysis1ListView.as_view(), name="analysis_1"),
    path("analysis2/", FilteredAnalysis2ListView.as_view(), name="analysis_2"),
    path("programmefilter/", FilteredProgrammeView.as_view(), name="programme_filter"),
    path(
        "interentityfilter/",
        FilteredInterEntityView.as_view(),
        name="inter_entity_filter",
    ),
    path("projectfilter/", FilteredProjectView.as_view(), name="project_filter"),
    path("fcofilter/", FilteredFCOMappingView.as_view(), name="fco_filter"),
    # Historical data
    path(
        "historicalnaturalcode/<year>/",
        HistoricalFilteredNACListView.as_view(),
        name="historical_natural_code",
    ),
    path(
        "historicalfinancecategory/<year>/",
        HistoricalFilteredExpenditureCategoryListView.as_view(),
        name="historical_finance_category",
    ),
    path(
        "historicalcommercialcategory/<year>/",
        HistoricalFilteredCommercialCategoryListView.as_view(),
        name="historical_commercial_category",
    ),
    path(
        "historicalanalysis1/<year>/",
        HistoricalFilteredAnalysis1ListView.as_view(),
        name="historical_analysis_1",
    ),
    path(
        "historicalanalysis2/<year>/",
        HistoricalFilteredAnalysis2ListView.as_view(),
        name="historical_analysis_2",
    ),
    path(
        "historicalprogrammefilter/<year>/",
        HistoricalFilteredProgrammeView.as_view(),
        name="historical_programme_filter",
    ),
    path(
        "historicalinterentityfilter/<year>/",
        HistoricalFilteredInterEntityView.as_view(),
        name="historical_inter_entity_filter",
    ),
    path(
        "historicalprojectfilter/<year>/",
        HistoricalFilteredProjectView.as_view(),
        name="historical_project_filter",
    ),
    path(
        "historicalfcofilter/<year>/",
        HistoricalFilteredFCOMappingView.as_view(),
        name="historical_fco_filter",
    ),
    path(
        "choose-year/",
        choose_year,
        name="chart_of_account_choose_year",
    ),
    path(
        "quick-links/<yyyy:year>/",
        quick_links,
        name="chart_of_account_quick_links",
    ),
]
