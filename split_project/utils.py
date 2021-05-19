from costcentre.models import CostCentre

from chartofaccountDIT.models import (
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)

from forecast.models import FinancialCode
from split_project.models import (
    ProjectSplitCoefficient,
    UploadProjectSplitCoefficient,
)


def validate():
    # Reservation.objects.values('day').annotate(cnt=Count('id')).filter(cnt__lte=5)
    too_large = (
        UploadProjectSplitCoefficient.objects.values(
            "financial_period", "financial_code_from"
        )
        .annotate(total="split_coefficient")
        .filter(total__gt=5)
    )
    return too_large


def create_split_data(
    cost_centre, nac, programme_code, project_code, coefficient, period_obj
):
    programme_obj = ProgrammeCode.objects.get(pk=programme_code)
    costcentre_obj = CostCentre.objects.get(pk=cost_centre)
    nac_obj = NaturalCode.objects.get(pk=nac)
    project_obj = ProjectCode.objects.get(pk=project_code)
    financial_code_from_obj, _ = FinancialCode.objects.get_or_create(
        programme=programme_obj,
        cost_centre=costcentre_obj,
        natural_account_code=nac_obj,
        project_code=None,
        analysis1_code=None,
        analysis2_code=None,
    )
    financial_code_from_obj.save()

    financial_code_to_obj, _ = FinancialCode.objects.get_or_create(
        programme=programme_obj,
        cost_centre=costcentre_obj,
        natural_account_code=nac_obj,
        project_code=project_obj,
        analysis1_code=None,
        analysis2_code=None,
    )
    financial_code_to_obj.save()
    project_split_obj = ProjectSplitCoefficient.objects.create(
        financial_period=period_obj,
        financial_code_from=financial_code_from_obj,
        financial_code_to=financial_code_to_obj,
        split_coefficient=coefficient,
    )
    project_split_obj.save()
    return project_split_obj
