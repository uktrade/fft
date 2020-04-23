from bootstrap_datepicker_plus import DatePickerInput

from django_filters import (
    DateFilter,
    ModelChoiceFilter,
    NumberFilter,
)

from core.filters import MyFilterSet

from gifthospitality.models import (
    GiftAndHospitality,
    GiftAndHospitalityCompany,
)


class GiftHospitalityFilter(MyFilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["id"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["category"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["classification"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["value"].widget.attrs.update(
            {"class": "govuk-input", }
        )

        self.form.fields["rep"].widget.attrs.update(
            {"class": "govuk-input", }
        )

        self.form.fields["grade"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["group"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["offer"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["company"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["action_taken"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["entered_date_stamp_from"].widget.attrs.update(
            {"class": "govuk-input", }
        )

        self.form.fields["entered_date_stamp_to"].widget.attrs.update(
            {"class": "govuk-input", }
        )

    entered_date_stamp_from = DateFilter(
        field_name="entered_date_stamp",
        label="Date Entered From:",
        lookup_expr="gte",
        widget=DatePickerInput(
            options={
                "format": "DD/MM/YYYY",  # moment date-time format
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            }
        ),
    )

    entered_date_stamp_to = DateFilter(
        field_name="entered_date_stamp",
        label="To:",
        lookup_expr="lte",
        widget=DatePickerInput(
            options={
                "format": "DD/MM/YYYY",  # moment date-time format
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            }
        ),
    )
    value = NumberFilter(lookup_expr="lte", label="Max value of offer (£)")

    # use a dropdown to search the following fields
    company = ModelChoiceFilter(queryset=GiftAndHospitalityCompany.objects.all())

    class Meta(MyFilterSet.Meta):
        model = GiftAndHospitality
        fields = [
            "id",
            "category",
            "classification",
            "value",
            "rep",
            "grade",
            "group",
            "offer",
            "company",
            "action_taken",
            "entered_date_stamp_from",
            "entered_date_stamp_to",
        ]
