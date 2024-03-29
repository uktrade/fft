import django_tables2 as tables

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedCommercialCategory,
    ArchivedExpenditureCategory,
    ArchivedFCOMapping,
    ArchivedInterEntity,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    InterEntity,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)
from core.tables import FadminTable


class ProgrammeTable(FadminTable):
    budget_type_descr = tables.Column(
        verbose_name="Budget Type",
        accessor="budget_type.budget_type",
    )

    class Meta(FadminTable.Meta):
        model = ProgrammeCode
        fields = (
            "programme_code",
            "programme_description",
            "budget_type_descr",
        )


class HistoricalProgrammeTable(ProgrammeTable):
    """The historical model is identical
    to the current one, so we can just
    inherit the class"""

    class Meta(ProgrammeTable.Meta):
        model = ArchivedProgrammeCode


class NaturalCodeTable(FadminTable):
    nac_category_description = tables.Column(
        verbose_name="Budget Grouping",
        accessor="expenditure_category.NAC_category.NAC_category_description",
    )
    budget_description = tables.Column(
        verbose_name="Budget Category",
        accessor="expenditure_category.grouping_description",
    )
    budget_NAC_code = tables.Column(
        verbose_name="Budget/Forecast NAC",
        accessor="expenditure_category.linked_budget_code.natural_account_code",
    )  # noqa: E501
    natural_account_code = tables.Column(verbose_name="PO/Actuals NAC")
    natural_account_code_description = tables.Column(verbose_name="NAC Description")
    op_delivery_plan = tables.Column(
        verbose_name="Operational Delivery Plan",
        accessor="expenditure_category.op_del_category.operating_delivery_description",  # noqa
    )

    class Meta(FadminTable.Meta):
        model = NaturalCode
        fields = (
            "economic_budget_code",
            "nac_category_description",
            "budget_description",
            "commercial_category",
            "op_delivery_plan",
            "budget_NAC_code",
            "natural_account_code",
            "natural_account_code_description",
        )


class HistoricalNaturalCodeTable(FadminTable):
    budget_description = tables.Column(
        verbose_name="Budget Category",
        accessor="expenditure_category.grouping_description",
    )

    class Meta(FadminTable.Meta):
        model = ArchivedNaturalCode
        fields = (
            "economic_budget_code",
            "NAC_category",
            "budget_description",
            "commercial_category",
            "op_delivery_plan",
            "account_L6_budget",
            "natural_account_code",
            "natural_account_code_description",
        )


class ExpenditureCategoryTable(FadminTable):
    nac_category = tables.Column(
        verbose_name="Budget Grouping",
        accessor="NAC_category.NAC_category_description",
    )

    class Meta(FadminTable.Meta):
        model = ExpenditureCategory
        fields = (
            "nac_category",
            "grouping_description",
            "description",
            "further_description",
        )


class HistoricalExpenditureCategoryTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = ArchivedExpenditureCategory
        fields = (
            "NAC_category",
            "grouping_description",
            "description",
            "further_description",
        )


class CommercialCategoryTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = CommercialCategory
        fields = ("commercial_category", "description")


class HistoricalCommercialCategoryTable(CommercialCategoryTable):
    """The historical model is identical
    to the current one, so we can just
    inherit the class"""

    class Meta(CommercialCategoryTable.Meta):
        model = ArchivedCommercialCategory


class Analysis2Table(FadminTable):
    class Meta(FadminTable.Meta):
        model = Analysis2
        fields = ("analysis2_code", "analysis2_description")


class HistoricalAnalysis2Table(Analysis2Table):
    """The historical model is identical
    to the current one, so we can just
    inherit the class"""

    class Meta(Analysis2Table.Meta):
        model = ArchivedAnalysis2


class Analysis1Table(FadminTable):
    analysis1_description = tables.Column(attrs={"th": {"id": "fiftypercent"}})

    class Meta(FadminTable.Meta):
        model = Analysis1
        fields = (
            "analysis1_code",
            "analysis1_description",
            "supplier",
            "pc_reference",
        )


class HistoricalAnalysis1Table(Analysis1Table):
    """The historical model is identical
    to the current one, so we can just
    inherit the class"""

    class Meta(Analysis1Table.Meta):
        model = ArchivedAnalysis1


class InterEntityTable(FadminTable):
    l1_value = tables.Column(
        verbose_name="L1 Value",
        accessor="l1_value.l1_value",
    )
    l1_description = tables.Column(
        verbose_name="L1 Description",
        accessor="l1_value.l1_description",
    )

    class Meta(FadminTable.Meta):
        model = InterEntity
        fields = (
            "l1_value",
            "l1_description",
            "l2_value",
            "l2_description",
            "cpid",
        )


class HistoricalInterEntityTable(InterEntityTable):
    l1_value = tables.Column(verbose_name="L1 Value", accessor="l1_value")
    l1_description = tables.Column(
        verbose_name="L1 Description", accessor="l1_description"
    )

    class Meta(InterEntityTable.Meta):
        model = ArchivedInterEntity


class ProjectTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = ProjectCode
        fields = ("project_code", "project_description")


class HistoricalProjectTable(ProjectTable):
    """The historical model is identical
    to the current one, so we can just
    inherit the class"""

    class Meta(ProjectTable.Meta):
        model = ArchivedProjectCode


class FCOMappingTable(FadminTable):
    oracle_code = tables.Column(
        verbose_name="DBT (Oracle) Code",
        accessor="account_L6_code_fk.natural_account_code",
    )
    oracle_description = tables.Column(
        verbose_name="DBT (Oracle) Description",
        accessor="account_L6_code_fk.natural_account_code_description",
    )

    nac_category_description = tables.Column(
        verbose_name="Budget Grouping",
        accessor="account_L6_code_fk.expenditure_category.NAC_category.NAC_category_description",  # noqa
    )
    budget_description = tables.Column(
        verbose_name="Budget Category",
        accessor="account_L6_code_fk.expenditure_category.grouping_description",
    )
    economic_budget_code = tables.Column(
        verbose_name="Expenditure Type",
        accessor="account_L6_code_fk.economic_budget_code",
    )

    class Meta(FadminTable.Meta):
        model = FCOMapping
        fields = (
            "economic_budget_code",
            "nac_category_description",
            "budget_description",
            "oracle_code",
            "oracle_description",
            "fco_code",
            "fco_description",
        )


class HistoricalFCOMappingTable(FCOMappingTable):
    oracle_code = tables.Column(
        verbose_name="Oracle Code",
        accessor="account_L6_code",
    )
    oracle_description = tables.Column(
        verbose_name="Oracle Description",
        accessor="account_L6_description",
    )

    nac_category_description = tables.Column(
        verbose_name="Budget Grouping",
        accessor="nac_category_description",
    )
    budget_description = tables.Column(
        verbose_name="Budget Category",
        accessor="budget_description",
    )
    economic_budget_code = tables.Column(
        verbose_name="Expenditure Type",
        accessor="economic_budget_code",
    )

    class Meta(FCOMappingTable.Meta):
        model = ArchivedFCOMapping
