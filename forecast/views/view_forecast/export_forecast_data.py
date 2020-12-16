from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse

from forecast.models import (
    ForecastingDataView,
)
from forecast.utils.access_helpers import (
    can_edit_cost_centre,
    can_view_forecasts,
)
from forecast.utils.export_helpers import (
    export_edit_to_excel,
    export_query_to_excel,
)
from forecast.utils.query_fields import ForecastQueryFields
from forecast.views.base import get_view_forecast_period_name


def get_period_for_title(period):
    if period:
        title = get_view_forecast_period_name(period)
    else:
        title = "Current"
    return f"({title})"


def export_forecast_data_generic(period, data_filter, title):
    fields = ForecastQueryFields(period)
    year = fields.selected_year
    datamodel = fields.datamodel

    q = datamodel.view_data.raw_data_annotated(
        fields.VIEW_FORECAST_DOWNLOAD_COLUMNS, data_filter, year=year
    )
    return export_query_to_excel(
        q, fields.VIEW_FORECAST_DOWNLOAD_COLUMNS, title, period
    )


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_dit(request, period):
    filter = {}
    title = f"DIT {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_group(request, group_code, period):
    fields = ForecastQueryFields(period)
    filter = {fields.group_code_field: group_code}
    title = f"{group_code} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_directorate(request, directorate_code, period):
    fields = ForecastQueryFields(period)
    filter = {fields.directorate_code_field: directorate_code}
    title = f"{directorate_code} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_cost_centre(request, cost_centre, period):
    fields = ForecastQueryFields(period)
    filter = {fields.cost_centre_code_field: cost_centre}
    title = f"{cost_centre} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_expenditure_detail_cost_centre(
    request, cost_centre, expenditure_category_id, budget_type_id, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.cost_centre_code_field: cost_centre,
        fields.budget_category_id_field: f"{expenditure_category_id}",
        fields.budget_type_field: f"{budget_type_id}",
    }
    title = f"{cost_centre} {get_period_for_title(period)} Expenditure"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_expenditure_detail_directorate(
    request, directorate_code, expenditure_category_id, budget_type_id, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.directorate_code_field: directorate_code,
        fields.budget_category_id_field: f"{expenditure_category_id}",
        fields.budget_type_field: f"{budget_type_id}",
    }
    title = f"{directorate_code} {get_period_for_title(period)} Expenditure"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_expenditure_detail_group(
    request, group_code, expenditure_category_id, budget_type_id, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.group_code_field: group_code,
        fields.budget_category_id_field: f"{expenditure_category_id}",
        fields.budget_type_field: f"{budget_type_id}",
    }
    title = f"{group_code} {get_period_for_title(period)} Expenditure"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_expenditure_dit(
    request, expenditure_category_id, budget_type_id, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.budget_category_id_field: f"{expenditure_category_id}",
        fields.budget_type_field: f"{budget_type_id}",
    }
    title = f"DIT {get_period_for_title(period)} Expenditure"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_programme_detail_directorate(
    request, directorate_code, programme_code_id, forecast_expenditure_type_name, period
):
    fields = ForecastQueryFields(period)

    filter = {
        fields.directorate_code_field: directorate_code,
        fields.programme_code_field: f"{programme_code_id}",
        fields.expenditure_type_name_field: f"{forecast_expenditure_type_name}",
    }

    title = f"{directorate_code} {programme_code_id} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_programme_detail_group(
    request, group_code, programme_code_id, forecast_expenditure_type_name, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.group_code_field: group_code,
        fields.programme_code_field: f"{programme_code_id}",
        fields.expenditure_type_name_field: f"{forecast_expenditure_type_name}",
    }
    title = f"{group_code} {programme_code_id} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_programme_detail_dit(
    request, programme_code_id, forecast_expenditure_type_name, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.programme_code_field: f"{programme_code_id}",
        fields.expenditure_type_name_field: f"{forecast_expenditure_type_name}",
    }
    title = f"DIT {programme_code_id} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_project_detail_cost_centre(
    request, cost_centre, project_code_id, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.cost_centre_code_field: cost_centre,
        fields.project_code_field: f"{project_code_id}",
    }
    title = f"{cost_centre} {project_code_id} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_project_detail_directorate(
    request, directorate_code, project_code_id, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.directorate_code_field: directorate_code,
        fields.project_code_field: f"{project_code_id}",
    }
    title = f"{directorate_code} {project_code_id} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_project_detail_group(
    request, group_code, project_code_id, period
):
    fields = ForecastQueryFields(period)
    filter = {
        fields.group_code_field: group_code,
        fields.project_code_field: f"{project_code_id}",
    }
    title = f"{group_code} {project_code_id} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


@user_passes_test(can_view_forecasts, login_url="index")
def export_forecast_data_project_detail_dit(request, project_code_id, period):
    fields = ForecastQueryFields(period)
    filter = {
        fields.project_code_field: f"{project_code_id}",
    }
    title = f"DIT {project_code_id} {get_period_for_title(period)}"
    return export_forecast_data_generic(period, filter, title)


def export_edit_forecast_data(request, cost_centre):
    fields = ForecastQueryFields()
    if can_edit_cost_centre(request.user, cost_centre):
        filter = {fields.cost_centre_code_field: cost_centre}
        q = ForecastingDataView.view_data.raw_data_annotated(
            {**fields.EDIT_KEYS_DOWNLOAD, **fields.EDIT_FORECAST_DOWNLOAD_COLUMNS},
            filter,
            order_list=fields.EDIT_FORECAST_DOWNLOAD_ORDER,
            include_zeros=True,
        )
        title = f"Edit forecast {cost_centre}"
        return export_edit_to_excel(
            q, fields.EDIT_KEYS_DOWNLOAD, fields.EDIT_FORECAST_DOWNLOAD_COLUMNS, title
        )
    else:
        return redirect(reverse("forecast_dit", kwargs={"period": 0, },))
