import json

from django import forms
from django.contrib.auth import get_user_model

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)
from core.forms import ChoicesWidget
from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year
from end_of_month.models import EndOfMonthStatus
from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
    UnlockedForecastEditor,
)


User = get_user_model()


class PublishForm(forms.Form):
    cost_centre_code = forms.IntegerField(widget=forms.HiddenInput(), initial=123)


class AddForecastRowForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.__cost_centre_code = kwargs.pop("cost_centre_code")
        self.__financial_year = kwargs.pop("financial_year")
        forms.Form.__init__(self, *args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        programme = cleaned_data.get("programme")
        natural_account_code = cleaned_data.get("natural_account_code")
        analysis1_code = cleaned_data.get("analysis1_code")
        analysis2_code = cleaned_data.get("analysis2_code")
        project_code = cleaned_data.get("project_code")

        financial_code = FinancialCode.objects.filter(
            programme=programme,
            natural_account_code=natural_account_code,
            analysis1_code=analysis1_code,
            analysis2_code=analysis2_code,
            project_code=project_code,
            cost_centre=self.__cost_centre_code,
        ).first()

        if financial_code:
            # Check if it used in the required year or not
            financial_amount_queryset = ForecastMonthlyFigure.objects.filter(
                financial_code=financial_code,
                financial_year_id=self.__financial_year,
                archived_status__isnull=True,
            ).first()
            budget_queryset = BudgetMonthlyFigure.objects.filter(
                financial_code=financial_code,
                financial_year_id=self.__financial_year,
                archived_status__isnull=True,
            ).first()

            if financial_amount_queryset or budget_queryset:
                raise forms.ValidationError(
                    "A row already exists with these details, "
                    "please amend the values you are supplying"
                )

    programme = forms.ModelChoiceField(
        queryset=ProgrammeCode.objects.filter(
            active=True,
        ),
        widget=ChoicesWidget,
        label="Programme description",
    )
    programme.widget.attrs.update(
        {"aria-describedby": "programme-hint programme-error"}
    )

    natural_account_code = forms.ModelChoiceField(
        queryset=NaturalCode.objects.filter(
            active=True,
        ),
        widget=ChoicesWidget,
        label="Natural Account Code description",
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
        widget=ChoicesWidget,
        label="Contract Reconciliation",
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
        widget=ChoicesWidget,
        label="Markets",
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
        widget=ChoicesWidget,
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

    def __init__(self, *args, **kwargs):
        super(UploadActualsForm, self).__init__(
            *args,
            **kwargs,
        )
        current_year = get_current_financial_year()
        self.fields["year"] = forms.ModelChoiceField(
            queryset=FinancialYear.objects.filter(
                financial_year__lte=current_year
            ).order_by("-financial_year"),
            empty_label="",
        )
        self.fields["year"].widget.attrs.update(
            {
                "class": "govuk-select",
                "aria-describedby": "year-hint year-error",
            }
        )


class UploadBudgetsForm(forms.Form):
    file = forms.FileField()
    file.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "file-hint file-error",
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


class PasteForecastForm(forms.Form):
    all_selected = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    pasted_at_row = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    paste_content = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def clean_pasted_at_row(self):
        data = self.cleaned_data["pasted_at_row"]

        if not data:
            return None

        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid row data supplied")

        return json_data


class EditForecastFigureForm(forms.Form):
    month = forms.IntegerField()
    amount = forms.IntegerField()
    natural_account_code = forms.IntegerField()
    programme_code = forms.CharField()
    project_code = forms.CharField(required=False)
    analysis1_code = forms.CharField(required=False)
    analysis2_code = forms.CharField(required=False)

    def clean_project_code(self):
        # Had to add this to prevent null coming through
        # as string - looks like a bug in Django
        project_code = self.cleaned_data["project_code"]

        if project_code == "null" or project_code == "":
            return None

        return project_code

    def clean_analysis1_code(self):
        # Had to add this to prevent null coming through
        # as string - looks like a bug in Django
        analysis1_code = self.cleaned_data["analysis1_code"]

        if analysis1_code == "null" or analysis1_code == "":
            return None

        return analysis1_code

    def clean_analysis2_code(self):
        # Had to add this to prevent null coming through
        # as string - looks like a bug in Django
        analysis2_code = self.cleaned_data["analysis2_code"]

        if analysis2_code == "null" or analysis2_code == "":
            return None

        return analysis2_code


class UnlockedForecastEditorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UnlockedForecastEditorForm, self).__init__(*args, **kwargs)

        unlocked_editors = UnlockedForecastEditor.objects.all()
        existing_editors = [editor.user.id for editor in unlocked_editors]

        finance_business_partners = User.objects.filter(
            groups__name="Finance Business Partner/BSCE",
        )
        id_list = [user.id for user in finance_business_partners]

        self.fields["user"].queryset = User.objects.filter(id__in=id_list).exclude(
            id__in=existing_editors
        )

    class Meta:
        model = UnlockedForecastEditor
        fields = [
            "user",
        ]


class ForecastPeriodForm(forms.Form):
    def __init__(self, *args, **kwargs):
        selected_period = kwargs.pop("selected_period", 0)
        super(ForecastPeriodForm, self).__init__(
            *args,
            **kwargs,
        )

        display_list: list[tuple[object, str]] = []

        # add future years
        display_list += FinancialYear.financial_year_objects.future_list()

        # add current year
        display_list.extend([(0, FinancialYear.objects.current().option_display)])

        archived_list = EndOfMonthStatus.archived_period_objects.archived_list()
        if archived_list:
            display_list.extend(archived_list)

        year_list = FinancialYear.financial_year_objects.archived_list()
        if year_list:
            display_list.extend(year_list)

        self.fields["selected_period"] = forms.ChoiceField(
            choices=display_list, initial=selected_period
        )
        self.fields["selected_period"].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )
