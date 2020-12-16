from django_filters import (
    DateFilter,
    ModelChoiceFilter,
    NumberFilter,
)

from django.forms import DateInput

from core.filters import MyFilterSet

from gifthospitality.models import (
    GiftAndHospitality,
    GiftAndHospitalityCompany,
)
from gifthospitality.utils.access_helpers import can_view_all_gifthospitality


class GiftHospitalityFilter(MyFilterSet):
    @property
    def qs(self):
        if not can_view_all_gifthospitality(self.request.user):
            return super(GiftHospitalityFilter,
                         self).qs.filter(entered_by=(self.request.user.first_name
                                         + " " + self.request.user.last_name))
        else:
            return super(GiftHospitalityFilter, self).qs.filter()

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
            {"class": "govuk-input govuk-!-width-one-thirds", }
        )

        self.form.fields["rep"].widget.attrs.update(
            {"class": "govuk-input govuk-!-width-one-thirds", }
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

        self.form.fields["company_name"].widget.attrs.update(
            {"class": "govuk-input", }
        )

        self.form.fields["action_taken"].widget.attrs.update(
            {"class": "govuk-select", }
        )

        self.form.fields["entered_date_stamp_from"].widget.attrs.update(
            {"class": "govuk-input govuk-!-width-one-thirds", }
        )

        self.form.fields["entered_date_stamp_to"].widget.attrs.update(
            {"class": "govuk-input govuk-!-width-one-thirds", }
        )

    entered_date_stamp_from = DateFilter(
        field_name="entered_date_stamp",
        label="Date Entered From:",
        lookup_expr="gte",
        widget=DateInput(
            attrs={
                "placeholder": "DD/MM/YYYY",
            },
        ),
    )

    entered_date_stamp_to = DateFilter(
        field_name="entered_date_stamp",
        label="To:",
        lookup_expr="lte",
        widget=DateInput(
            attrs={
                "placeholder": "DD/MM/YYYY",
            },
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
            "company_name",
            "action_taken",
            "entered_date_stamp_from",
            "entered_date_stamp_to",
        ]
