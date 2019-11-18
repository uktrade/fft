from django import forms

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)

from core.models import FinancialYear
from core.myutils import (
    get_current_financial_year,
)

from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)


class EditForm(forms.Form):
    cell_data = forms.CharField(widget=forms.Textarea)
    cost_centre_code = forms.IntegerField(widget=forms.HiddenInput(), initial=123)
    financial_year = forms.IntegerField(widget=forms.HiddenInput(), initial=123)


class AddForecastRowForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        programme = cleaned_data.get("programme")
        natural_account_code = cleaned_data.get("natural_account_code")
        analysis1_code = cleaned_data.get("analysis1_code")
        analysis2_code = cleaned_data.get("analysis2_code")
        project_code = cleaned_data.get("project_code")

        existing_row_count = MonthlyFigure.objects.filter(
            financial_year_id=get_current_financial_year(),
            programme=programme,
            natural_account_code=natural_account_code,
            analysis1_code=analysis1_code,
            analysis2_code=analysis2_code,
            project_code=project_code,
        ).count()

        if existing_row_count > 0:
            raise forms.ValidationError(
                "A row already exists with these details, "
                "please amend the values you are supplying"
            )

    programme = forms.ModelChoiceField(
        queryset=ProgrammeCode.objects.filter(
            active=True,
        ),
        empty_label="",
    )
    programme.widget.attrs.update(
        {"class": "govuk-select", "aria-describedby": "programme-hint programme-error"}
    )

    natural_account_code = forms.ModelChoiceField(
        queryset=NaturalCode.objects.filter(
            active=True,
        ),
        empty_label="",
    )
    natural_account_code.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "natural_account_code-hint natural_account_code-error",
        }
    )

    analysis1_code = forms.ModelChoiceField(
        queryset=Analysis1.objects.filter(
            active=True,
        ),
        required=False,
        empty_label="",
    )
    analysis1_code.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "analysis1_code-hint analysis1_code-error",
        }
    )

    analysis2_code = forms.ModelChoiceField(
        queryset=Analysis2.objects.filter(
            active=True,
        ),
        required=False,
        empty_label="",
    )
    analysis2_code.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "analysis2_code-hint analysis2_code-error",
        }
    )

    project_code = forms.ModelChoiceField(
        queryset=ProjectCode.objects.all(),
        required=False,
        empty_label="",
    )
    project_code.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "project_code-hint project_code-error",
        }
    )


class UploadActualsForm(forms.Form):
    file = forms.FileField()
    file.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "file-hint file-error",
        }
    )

    period = forms.ModelChoiceField(
        queryset=FinancialPeriod.objects.all(),
        empty_label="",
    )
    period.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "period-hint period-error",
        }
    )

    year = forms.ModelChoiceField(
        queryset=FinancialYear.objects.all(),
        empty_label="",
    )
    year.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "year-hint year-error",
        }
    )
