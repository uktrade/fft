from forecast.models import ForecastingDataView
from forecast.utils.export_helpers import (
    export_edit_to_excel,
    export_query_to_excel,
)
from forecast.utils.query_fields import (
    COST_CENTRE_CODE,
    DIRECTORATE_CODE,
    EDIT_FORECAST_DOWNLOAD_COLUMNS,
    EDIT_FORECAST_DOWNLOAD_ORDER,
    EDIT_KEYS_DOWNLOAD,
    GROUP_CODE,
    VIEW_FORECAST_DOWNLOAD_COLUMNS,
)


def export_forecast_data_dit(request):
    q = ForecastingDataView.view_data.raw_data_annotated(VIEW_FORECAST_DOWNLOAD_COLUMNS)
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, "DIT")


def export_forecast_data_group(request, group_code):
    filter = {GROUP_CODE: group_code}
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, group_code)


def export_forecast_data_directorate(request, directorate_code):
    filter = {DIRECTORATE_CODE: directorate_code}
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, directorate_code)


def export_forecast_data_cost_centre(request, cost_centre):
    filter = {COST_CENTRE_CODE: cost_centre}
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, cost_centre)


def export_edit_forecast_data(request, cost_centre):
    filter = {COST_CENTRE_CODE: cost_centre}
    q = ForecastingDataView.view_data.raw_data_annotated(
        {**EDIT_KEYS_DOWNLOAD, **EDIT_FORECAST_DOWNLOAD_COLUMNS},
        filter,
        order_list=EDIT_FORECAST_DOWNLOAD_ORDER,
        include_zeros=True,
    )
    title = f'Edit forecast {cost_centre}'
    return export_edit_to_excel(q,
                                EDIT_KEYS_DOWNLOAD,
                                EDIT_FORECAST_DOWNLOAD_COLUMNS,
                                title)
