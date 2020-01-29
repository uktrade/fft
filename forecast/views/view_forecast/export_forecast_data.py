from forecast.models import ForecastBudgetDataView
from forecast.utils.export_helpers import (
    export_edit_to_excel,
    export_query_to_excel,
)
from forecast.utils.query_fields import (
    COST_CENTRE_CODE,
    DIRECTORATE_CODE,
    EDIT_FORECAST_DOWNLOAD_COLUMNS,
    EDIT_KEYS_DOWNLOAD,
    GROUP_CODE,
    VIEW_FORECAST_DOWNLOAD_COLUMNS,
)


def export_forecast_data_dit(request):
    q = ForecastBudgetDataView.view_data.raw_data(VIEW_FORECAST_DOWNLOAD_COLUMNS)
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, "DIT")


def export_forecast_data_group(request, group_code):
    filter = {GROUP_CODE: group_code}
    q = ForecastBudgetDataView.view_data.raw_data(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, group_code)


def export_forecast_data_directorate(request, directorate_code):
    filter = {DIRECTORATE_CODE: directorate_code}
    q = ForecastBudgetDataView.view_data.raw_data(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, directorate_code)


def export_forecast_data_cost_centre(request, cost_centre):
    filter = {COST_CENTRE_CODE: cost_centre}
    q = ForecastBudgetDataView.view_data.raw_data(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, cost_centre)


def export_edit_forecast_data(request, cost_centre):
    filter = {COST_CENTRE_CODE: cost_centre}
    q = ForecastBudgetDataView.view_data.raw_data(
        {**EDIT_KEYS_DOWNLOAD, **EDIT_FORECAST_DOWNLOAD_COLUMNS}, filter)
    return export_edit_to_excel(q,
                                EDIT_KEYS_DOWNLOAD,
                                EDIT_FORECAST_DOWNLOAD_COLUMNS,
                                cost_centre)
