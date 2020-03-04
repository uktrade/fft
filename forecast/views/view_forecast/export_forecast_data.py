from forecast.models import ForecastingDataView
from forecast.utils.export_helpers import (
    export_edit_to_excel,
    export_query_to_excel,
)
from forecast.utils.query_fields import (
    BUDGET_CATEGORY_ID,
    BUDGET_TYPE,
    COST_CENTRE_CODE,
    DIRECTORATE_CODE,
    EDIT_FORECAST_DOWNLOAD_COLUMNS,
    EDIT_FORECAST_DOWNLOAD_ORDER,
    EDIT_KEYS_DOWNLOAD,
    FORECAST_EXPENDITURE_TYPE_NAME,
    GROUP_CODE,
    PROGRAMME_CODE,
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


def export_forecast_data_programme_details(request, cost_centre):
    filter = {COST_CENTRE_CODE: cost_centre}
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, cost_centre)


def export_forecast_data_expenditure_detail_cost_centre(
    request,
    cost_centre,
    expenditure_category_id,
    budget_type_id
):
    filter = {
        COST_CENTRE_CODE: cost_centre,
        BUDGET_CATEGORY_ID: f"{expenditure_category_id}",
        BUDGET_TYPE: f"{budget_type_id}",
    }
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    title = f'{cost_centre}  Expenditure'
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, title)


def export_forecast_data_expenditure_detail_directorate(
    request,
    directorate_code,
    expenditure_category_id,
    budget_type_id
):
    filter = {
        DIRECTORATE_CODE: directorate_code,
        BUDGET_CATEGORY_ID: f"{expenditure_category_id}",
        BUDGET_TYPE: f"{budget_type_id}",
    }
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    title = f'{directorate_code}  Expenditure'
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, title)


def export_forecast_data_expenditure_detail_group(
    request,
    group_code,
    expenditure_category_id,
    budget_type_id
):
    filter = {
        GROUP_CODE: group_code,
        BUDGET_CATEGORY_ID: f"{expenditure_category_id}",
        BUDGET_TYPE: f"{budget_type_id}",
    }
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    title = f'{group_code}  Expenditure'
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, title)


def export_forecast_data_expenditure_dit(
    request,
    expenditure_category_id,
    budget_type_id
):
    filter = {
        BUDGET_CATEGORY_ID: f"{expenditure_category_id}",
        BUDGET_TYPE: f"{budget_type_id}",
    }
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    title = f'DIT  Expenditure'
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, title)


def export_forecast_data_programme_detail_directorate(
    request,
    directorate_code,
    programme_code_id,
    forecast_expenditure_type_name
):
    filter = {
        DIRECTORATE_CODE: directorate_code,
        PROGRAMME_CODE: f"{programme_code_id}",
        FORECAST_EXPENDITURE_TYPE_NAME: f"{forecast_expenditure_type_name}",
    }
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    title = f'{directorate_code} {programme_code_id}'
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, title)


def export_forecast_data_programme_detail_group(
    request,
    group_code,
    programme_code_id,
    forecast_expenditure_type_name
):
    filter = {
        GROUP_CODE: group_code,
        PROGRAMME_CODE: f"{programme_code_id}",
        FORECAST_EXPENDITURE_TYPE_NAME: f"{forecast_expenditure_type_name}",
    }
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    title = f'{group_code} {programme_code_id}'
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, title)


def export_forecast_data_programme_detail_dit(
    request,
    programme_code_id,
    forecast_expenditure_type_name
):
    filter = {
        PROGRAMME_CODE: f"{programme_code_id}",
        FORECAST_EXPENDITURE_TYPE_NAME: f"{forecast_expenditure_type_name}",
    }
    q = ForecastingDataView.view_data.raw_data_annotated(
        VIEW_FORECAST_DOWNLOAD_COLUMNS, filter
    )
    title = f'DIT {programme_code_id}'
    return export_query_to_excel(q, VIEW_FORECAST_DOWNLOAD_COLUMNS, title)


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
