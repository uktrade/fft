import datetime

from django.db import models

from chartofaccountDIT.models import BudgetType
from core.metamodels import ArchivedModel, IsActiveModel


class OrganizationCode(IsActiveModel):
    organization_code = models.CharField(max_length=50, verbose_name="Organization")
    organization_alias = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.organization_code} - {self.organization_alias}"


# Treasury data
class SegmentGrandParent(IsActiveModel):
    segment_grand_parent_code = models.CharField(
        max_length=8, primary_key=True, verbose_name="segment grand parent code"
    )
    segment_grand_parent_long_name = models.CharField(
        max_length=255, verbose_name="segment grandparent long name"
    )
    segment_department_code = models.CharField(
        max_length=20, verbose_name="segment department code", default=""
    )
    segment_department_long_name = models.CharField(
        max_length=255, verbose_name="segment department long name", default=""
    )

    def __str__(self):
        return self.segment_grand_parent_code


class SegmentParent(IsActiveModel):
    segment_parent_code = models.CharField(
        max_length=8, primary_key=True, verbose_name="segment parent code"
    )
    segment_parent_long_name = models.CharField(
        max_length=255, verbose_name="segment parent long name"
    )
    segment_grand_parent_code = models.ForeignKey(
        SegmentGrandParent, on_delete=models.PROTECT
    )

    def __str__(self):
        return "{} - {}".format(self.segment_parent_code, self.segment_parent_long_name)


class Segment(IsActiveModel):
    segment_code = models.CharField(
        max_length=8, primary_key=True, verbose_name="segment code"
    )
    segment_long_name = models.CharField(
        max_length=255, verbose_name="segment long name"
    )
    segment_parent_code = models.ForeignKey(SegmentParent, on_delete=models.PROTECT)

    organization = models.ForeignKey(
        OrganizationCode,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.segment_long_name


class EstimateRow(IsActiveModel):
    estimate_row_code = models.CharField(
        max_length=8, primary_key=True, verbose_name="estimates row code"
    )
    estimate_row_long_name = models.CharField(
        max_length=255, verbose_name="estimates row long name"
    )
    sort_order = models.IntegerField(verbose_name="sort order", default=9999)

    def __str__(self):
        return self.estimate_row_code


class SubSegmentAbstract(models.Model):
    VOTED = "VT"
    NON_VOTED = "NVT"
    UNDEF = "N/A"
    CONTROL_ACCOUNTING_AUTH_CHOICES = (
        (VOTED, "VOTED"),
        (
            NON_VOTED,
            (
                ("NON - VOTED_DEPT", "NON - VOTED_DEPT"),
                ("NON-VOTED_CFER", "NON-VOTED_CFER"),
                ("NON-VOTED_CF", "NON-VOTED_CF"),
                ("NON-VOTED_PC", "NON-VOTED_PC"),
                ("NON-VOTED_NIF", "NON-VOTED_NIF"),
                ("NON-VOTED_NLF", "NON-VOTED_NLF"),
                ("NON-VOTED_CEX", "NON-VOTED_CEX"),
                ("NON-VOTED_SF", "NON-VOTED_SF"),
                ("NON-VOTED_LG", "NON-VOTED_LG"),
                ("NON-VOTED_DA", "NON-VOTED_DA"),
            ),
        ),
        (UNDEF, UNDEF),
    )

    DEL = "DEL"
    AME = "AME"
    NB = "NON-BUDGET"
    DELADM = "DEL ADMIN"
    DELPROG = "DEL PROG"
    AMEDEPT = "DEPT AME"
    AMENODEPT = "NON-DEPT AME"
    CONTROL_BUDGET_CHOICES = (
        (DEL, ((DELADM, "DEL ADMIN"), (DELPROG, "DEL PROG"))),
        (AME, ((AMEDEPT, "DEPT AME"), (AMENODEPT, "NON-DEPT AME"))),
        (NB, NB),
    )
    sub_segment_code = models.CharField(
        max_length=8, primary_key=True, verbose_name="sub segment code"
    )
    sub_segment_long_name = models.CharField(
        max_length=255, verbose_name="sub segment long name"
    )
    control_budget_detail_code = models.CharField(
        max_length=50,
        choices=CONTROL_BUDGET_CHOICES,
        default=NB,
        verbose_name="control budget detail code",
    )
    accounting_authority_code = models.CharField(
        max_length=255, verbose_name="accounting authority code"
    )
    accounting_authority_DetailCode = models.CharField(
        max_length=255,
        choices=CONTROL_ACCOUNTING_AUTH_CHOICES,
        default=UNDEF,
        verbose_name="accounting authority detail code",
    )
    # the following field is used to link the sub-segment
    # to the DIT programme codes, to create the Oscar
    # report its value could be derived from Control
    # Budget, but it is easier to have an independent fields.
    # there are only a handful of sub-segments, so the
    # maintenance of this field is not a problem!
    dit_budget_type = models.ForeignKey(
        BudgetType,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="DBT Budget Code (used to generate the Oscar return)",
    )

    class Meta:
        abstract = True


class SubSegment(SubSegmentAbstract, IsActiveModel):
    Segment_code = models.ForeignKey(Segment, on_delete=models.PROTECT)
    estimates_row_code = models.ForeignKey(EstimateRow, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("Segment_code", "dit_budget_type")
        verbose_name = "Sub Segment"

    def __str__(self):
        return f"{self.sub_segment_code} - {self.sub_segment_long_name}"


class ArchivedSubSegment(SubSegmentAbstract, ArchivedModel):
    segment_grand_parent_code = models.CharField(
        max_length=8, verbose_name="segment grand parent code"
    )
    segment_grand_parent_long_name = models.CharField(
        max_length=255, verbose_name="segment grandparent long name"
    )
    segment_department_code = models.CharField(
        max_length=20, verbose_name="segment department code", default=""
    )
    segment_department_long_name = models.CharField(
        max_length=255, verbose_name="segment department long name", default=""
    )
    segment_parent_code = models.CharField(
        max_length=8, verbose_name="segment parent code"
    )
    segment_parent_long_name = models.CharField(
        max_length=255, verbose_name="segment parent long name"
    )
    segment_code = models.CharField(max_length=8, verbose_name="segment code")
    segment_long_name = models.CharField(
        max_length=255, verbose_name="segment long name"
    )
    organization_code = models.CharField(max_length=50, verbose_name="Organization")
    organization_alias = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    estimate_row_code = models.CharField(
        max_length=8, verbose_name="estimates row code"
    )
    estimate_row_long_name = models.CharField(
        max_length=255, verbose_name="estimates row long name"
    )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        archived_time = datetime.datetime.now()
        segment_hist = cls(
            created=obj.created,
            archived=archived_time,
            financial_year=year_obj,
            sub_segment_code=obj.sub_segment_code,
            sub_segment_long_name=obj.sub_segment_long_name + suffix,
            control_budget_detail_code=obj.control_budget_detail_code,
            accounting_authority_code=obj.accounting_authority_code,
            accounting_authority_DetailCode=obj.accounting_authority_DetailCode,
            dit_budget_type=obj.dit_budget_type,
            segment_grand_parent_code=obj.Segment_code.segment_parent_code.segment_grand_parent_code.segment_grand_parent_code,  # noqa
            segment_grand_parent_long_name=obj.Segment_code.segment_parent_code.segment_grand_parent_code.segment_grand_parent_long_name,  # noqa
            segment_department_code=obj.Segment_code.segment_parent_code.segment_grand_parent_code.segment_department_code,  # noqa
            segment_department_long_name=obj.Segment_code.segment_parent_code.segment_grand_parent_code.segment_department_long_name,  # noqa
            segment_parent_code=obj.Segment_code.segment_parent_code.segment_parent_code,  # noqa
            segment_parent_long_name=obj.Segment_code.segment_parent_code.segment_parent_long_name,  # noqa
            segment_code=obj.Segment_code.segment_code,
            segment_long_name=obj.Segment_code.segment_long_name,
            organization_code=obj.Segment_code.organization.organization_code,
            organization_alias=obj.Segment_code.organization.organization_alias,
            estimate_row_code=obj.estimates_row_code.estimate_row_code,
            estimate_row_long_name=obj.estimates_row_code.estimate_row_long_name,
        )
        segment_hist.save()
        return segment_hist

    def __str__(self):
        return (
            f"{self.sub_segment_code} - "
            f"{self.sub_segment_long_name} "
            f"{self.financial_year.financial_year_display}"
        )

    class Meta:
        unique_together = ("segment_code", "dit_budget_type", "financial_year")
        verbose_name = "Archived Treasury Segment"
