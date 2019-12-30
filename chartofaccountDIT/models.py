from django.db import models

from core.metamodels import (
    ArchivedModel,
    LogChangeModel,
    TimeStampedModel,
)

from treasuryCOA.models import L5Account


# Other members of Account Codes
class Analysis1Abstract(models.Model):
    analysis1_code = models.CharField(
        "Contract Code",
        primary_key=True,
        max_length=50,
    )
    analysis1_description = models.CharField(
        "Contract Name",
        max_length=300,
    )
    supplier = models.CharField(
        "Supplier",
        max_length=300,
        default="",
    )
    pc_reference = models.CharField(
        "PC Reference",
        max_length=300,
        default="",
    )

    def __str__(self):
        return "{} - {}".format(
            self.analysis1_code,
            self.analysis1_description,
        )

    class Meta:
        abstract = True
        verbose_name_plural = "Contract Reconciliations (Analysis 1)"
        verbose_name = "Contract Reconciliation (Analysis 1)"
        ordering = ["analysis1_code"]


class Analysis1(Analysis1Abstract, TimeStampedModel, LogChangeModel):
    pass


class HistoricalAnalysis1(Analysis1Abstract, ArchivedModel):
    analysis1_code = models.CharField("Contract Code", max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(
            super().__str__(), self.financial_year.financial_year_display
        )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        obj_hist = cls(
            analysis1_description="{}{}".format(obj.analysis1_description, suffix),
            analysis1_code=obj.analysis1_code,
            supplier=obj.supplier,
            pc_reference=obj.pc_reference,
            financial_year=year_obj,
            active=obj.active,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name_plural = "Historical Contract Reconciliations (Analysis 1)"
        verbose_name = "Historical Contract Reconciliation (Analysis 1)"
        ordering = ["financial_year", "analysis1_code"]


class Analysis2Abstract(models.Model):
    analysis2_code = models.CharField("Market Code", primary_key=True, max_length=50)
    analysis2_description = models.CharField(max_length=300, verbose_name="Market")

    def __str__(self):
        return "{} - {}".format(self.analysis2_code, self.analysis2_description)

    class Meta:
        abstract = True
        verbose_name = "Market (Analysis 2)"
        verbose_name_plural = "Markets (Analysis 2)"
        ordering = ["analysis2_code"]


class Analysis2(Analysis2Abstract, TimeStampedModel):
    pass


class HistoricalAnalysis2(Analysis2Abstract, ArchivedModel):
    analysis2_code = models.CharField("Contract Code", max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "{}{}".format(
            super().__str__(),
            self.financial_year.financial_year_display,
        )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        obj_hist = cls(
            analysis2_description=obj.analysis2_description + suffix,
            analysis2_code=obj.analysis2_code,
            financial_year=year_obj,
            active=obj.active,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Historical Market (Analysis 2)"
        verbose_name_plural = "Historical Markets (Analysis 2)"
        ordering = ["financial_year", "analysis2_code"]


# Category defined by DIT
class NACCategory(TimeStampedModel, LogChangeModel):
    NAC_category_description = models.CharField(
        max_length=255, verbose_name="Budget Grouping", unique=True
    )

    def __str__(self):
        return str(self.NAC_category_description)

    class Meta:
        verbose_name = "Budget Grouping"
        verbose_name_plural = "Budget Groupings"
        ordering = ["NAC_category_description"]


class OperatingDeliveryCategory(TimeStampedModel, LogChangeModel):
    """Another way to classify the Budget NACs"""

    operating_delivery_description = models.CharField(
        max_length=255,
        verbose_name="Operating Delivery Plan Category",
        unique=True,
    )

    def __str__(self):
        return str(self.operating_delivery_description)

    class Meta:
        verbose_name = "Operating Delivery Plan Category"
        verbose_name_plural = "Operating Delivery Plan Categories"
        ordering = ["operating_delivery_description"]


class ExpenditureCategoryAbstract(models.Model):
    grouping_description = models.CharField(
        max_length=255, verbose_name="Budget Category", unique=True
    )
    description = models.CharField(max_length=5000, blank=True, null=True)
    further_description = models.CharField(
        max_length=5000,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.grouping_description)

    class Meta:
        abstract = True
        verbose_name = "Budget Category"
        verbose_name_plural = "Budget Categories"
        ordering = ["grouping_description"]


class ExpenditureCategory(
    ExpenditureCategoryAbstract, TimeStampedModel, LogChangeModel
):
    linked_budget_code = models.ForeignKey(
        "NaturalCode",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Budget Code",
    )
    NAC_category = models.ForeignKey(
        NACCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Budget Grouping",
    )
    op_del_category = models.ForeignKey(
        OperatingDeliveryCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Operating Delivery Plan",
    )


class HistoricalExpenditureCategory(
    ExpenditureCategoryAbstract,
    ArchivedModel,
):
    linked_budget_code = models.IntegerField(verbose_name="Budget Code")
    linked_budget_code_description = models.CharField(
        max_length=200, verbose_name="Budget Description"
    )
    NAC_category = models.CharField(
        max_length=255,
        verbose_name="Budget Grouping",
    )
    active = models.BooleanField(default=False)

    def __str__(self):
        return "{}{}".format(
            super().__str__(),
            self.financial_year.financial_year_display,
        )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        obj_hist = cls(
            financial_year=year_obj,
            active=obj.active,
            grouping_description=obj.grouping_description + suffix,
            NAC_category=obj.NAC_category.NAC_category_description,
            description=obj.description,
            further_description=obj.further_description,
            linked_budget_code=obj.linked_budget_code.natural_account_code,
            linked_budget_code_description=obj.linked_budget_code.natural_account_code_description, # noqa
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Historic Budget Category"
        verbose_name_plural = "Historic Budget Categories"
        ordering = ["financial_year", "grouping_description"]


class CommercialCategoryAbstract(models.Model):
    commercial_category = models.CharField(
        max_length=255,
        verbose_name="Commercial Category",
        unique=True,
    )
    description = models.CharField(
        max_length=5000,
        blank=True,
        null=True,
    )
    approvers = models.CharField(
        max_length=5000,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.commercial_category)

    class Meta:
        abstract = True
        verbose_name = "Commercial Category"
        verbose_name_plural = "Commercial Categories"
        ordering = ["commercial_category"]


class CommercialCategory(
    CommercialCategoryAbstract,
    TimeStampedModel,
    LogChangeModel,
):
    pass


class HistoricalCommercialCategory(
    CommercialCategoryAbstract,
    ArchivedModel,
):
    active = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(
            super().__str__(), self.financial_year.financial_year_display
        )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        obj_hist = cls(
            commercial_category=obj.commercial_category + suffix,
            description=obj.description,
            approvers=obj.approvers,
            financial_year=year_obj,
            active=obj.active,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Historic Commercial Category"
        verbose_name_plural = "Historic Commercial Categories"
        ordering = ["financial_year", "commercial_category"]


# define level1 values: Capital, staff, etc is Level 1 in UKTI nac hierarchy
class NaturalCodeAbstract(models.Model):
    natural_account_code = models.IntegerField(
        primary_key=True,
        verbose_name="NAC",
    )
    natural_account_code_description = models.CharField(
        max_length=200, verbose_name="NAC Description"
    )
    used_for_budget = models.BooleanField(default=False)

    economic_budget_code = models.CharField(
        max_length=255,
        verbose_name="Expenditure Type",
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{} - {}".format(
            self.natural_account_code, self.natural_account_code_description
        )

    class Meta:
        abstract = True
        verbose_name = "Natural Account Code (NAC)"
        verbose_name_plural = "Natural Account Codes (NAC)"
        ordering = ["natural_account_code"]


class NaturalCode(NaturalCodeAbstract, TimeStampedModel, LogChangeModel):
    expenditure_category = models.ForeignKey(
        ExpenditureCategory,
        verbose_name="Budget Category",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    commercial_category = models.ForeignKey(
        CommercialCategory, on_delete=models.PROTECT, blank=True, null=True
    )
    account_L5_code = models.ForeignKey(
        L5Account, on_delete=models.PROTECT, blank=True, null=True
    )
    account_L5_code_upload = models.ForeignKey(
        L5Account,
        on_delete=models.PROTECT,
        verbose_name="L5 for OSCAR upload",
        related_name="L5_OSCAR_Upload",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        # Override save to copy the economic budget code, for convenience.
        link_l5_code = None
        if self.account_L5_code:
            link_l5_code = self.account_L5_code.account_l5_code
        else:
            if self.account_L5_code_upload:
                link_l5_code = self.account_L5_code_upload.account_l5_code

        if link_l5_code:
            l5_linked = L5Account.objects.get(
                account_l5_code=link_l5_code,
            )
            self.economic_budget_code = l5_linked.economic_budget_code
        super(NaturalCode, self).save(*args, **kwargs)


class HistoricalNaturalCode(NaturalCodeAbstract, ArchivedModel):
    """It includes the fields displayed on the FIDO interface,
    and it has no foreign keys in it, to avoid dependencies
    from other tables. The tables is not normalised by design."""

    natural_account_code = models.IntegerField(verbose_name="PO/Actuals NAC")
    expenditure_category = models.CharField(
        max_length=255, verbose_name="Budget Category", blank=True, null=True
    )
    NAC_category = models.CharField(
        max_length=255, verbose_name="Budget Grouping", blank=True, null=True
    )
    commercial_category = models.CharField(
        max_length=255, verbose_name="Commercial Category", blank=True, null=True
    )
    account_L5_code = models.BigIntegerField(blank=True, null=True)
    account_L5_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    account_L6_budget = models.BigIntegerField(
        "Budget/Forecast NAC", blank=True, null=True
    )
    account_L5_code_upload = models.BigIntegerField(
        verbose_name="L5 for OSCAR upload", blank=True, null=True
    )
    active = models.BooleanField(default=False)

    def __str__(self):
        return super().__str__() + " " + self.financial_year.financial_year_display

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        if obj.expenditure_category:
            expenditure_category_value = obj.expenditure_category.grouping_description  # noqa
            NAC_category_val = (
                obj.expenditure_category.NAC_category.NAC_category_description
            )
            account_L6_budget_val = (
                obj.expenditure_category.linked_budget_code.natural_account_code
            )
        else:
            expenditure_category_value = None
            NAC_category_val = None
            account_L6_budget_val = None
        if obj.commercial_category:
            commercial_category_val = obj.commercial_category.commercial_category
        else:
            commercial_category_val = None
        if obj.account_L5_code_upload:
            account_L5_code_upload_val = obj.account_L5_code_upload.account_l5_code
        else:
            account_L5_code_upload_val = None
        if obj.account_L5_code:
            account_L5_code_val = obj.account_L5_code.account_l5_code
            account_L5_description_val = obj.account_L5_code.account_l5_long_name
        else:
            account_L5_code_val = None
            account_L5_description_val = None
        obj_hist = cls(
            natural_account_code_description=obj.natural_account_code_description + suffix,  # noqa
            natural_account_code=obj.natural_account_code,
            used_for_budget=obj.used_for_budget,
            expenditure_category=expenditure_category_value,
            NAC_category=NAC_category_val,
            commercial_category=commercial_category_val,
            account_L6_budget=account_L6_budget_val,
            account_L5_code=account_L5_code_val,
            account_L5_description=account_L5_description_val,
            account_L5_code_upload=account_L5_code_upload_val,
            economic_budget_code=obj.economic_budget_code,
            financial_year=year_obj,
            active=obj.active,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Historic Natural Account Code (NAC)"
        verbose_name_plural = "Historic Natural Account Codes (NAC)"
        ordering = ["financial_year", "natural_account_code"]


class BudgetType(models.Model):
    budget_type_key = models.CharField("Key", primary_key=True, max_length=50)
    budget_type = models.CharField("Budget Type", max_length=100)
    budget_type_display = models.CharField(max_length=100, blank=True, null=True)
    budget_type_display_order = models.IntegerField(default=99)

    def __str__(self):
        return self.budget_type


class ProgrammeCodeAbstract(models.Model):
    programme_code = models.CharField(
        "Programme Code",
        primary_key=True,
        max_length=50,
    )
    programme_description = models.CharField(
        "Programme Name",
        max_length=100,
    )

    def __str__(self):
        return self.programme_code + " - " + self.programme_description

    class Meta:
        abstract = True
        verbose_name = "Programme Code"
        verbose_name_plural = "Programme Codes"
        ordering = ["programme_code"]


class ProgrammeCode(ProgrammeCodeAbstract, TimeStampedModel, LogChangeModel):
    # TODO - remove "fk" add related name
    budget_type_fk = models.ForeignKey(
        BudgetType,
        verbose_name="Budget Type",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )


class HistoricalProgrammeCode(ProgrammeCodeAbstract, ArchivedModel):
    programme_code = models.CharField("Programme Code", max_length=50)
    active = models.BooleanField(default=False)
    budget_type = models.CharField("Budget Type", max_length=100)

    def __str__(self):
        s = super().__str__()
        return s + " " + self.financial_year.financial_year_display

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        pc_hist = cls(
            programme_code=obj.programme_code,
            programme_description="{}{}".format(
                obj.programme_description,
                suffix,
            ),
            budget_type=obj.budget_type_fk.budget_type,
            active=obj.active,
            financial_year=year_obj,
        )
        pc_hist.save()
        return pc_hist

    class Meta:
        verbose_name = "Historic Programme Code"
        verbose_name_plural = "Historic Programme Codes"
        ordering = ["financial_year", "programme_code"]


class InterEntityL1(TimeStampedModel, LogChangeModel):
    l1_value = models.CharField(
        "Government Body",
        primary_key=True,
        max_length=10,
    )
    l1_description = models.CharField(
        "Government Body Description",
        max_length=100,
    )

    def __str__(self):
        return self.l1_value + " - " + self.l1_description

    class Meta:
        verbose_name = "Government Body"
        verbose_name_plural = "Government Bodies"
        ordering = ["l1_value"]


class InterEntityAbstract(models.Model):
    l2_value = models.CharField(
        "ORACLE - Inter Entity Code",
        primary_key=True,
        max_length=10,
    )
    l2_description = models.CharField(
        "ORACLE - Inter Entity Description",
        max_length=100,
    )
    cpid = models.CharField(
        "Treasury - CPID (Departmental Code No.)",
        max_length=10,
    )

    def __str__(self):
        return self.l2_value + " - " + self.l2_description

    class Meta:
        abstract = True
        verbose_name = "Inter-Entity"
        verbose_name_plural = "Inter-Entities"
        ordering = ["l2_value"]


class InterEntity(InterEntityAbstract, TimeStampedModel, LogChangeModel):
    l1_value = models.ForeignKey(InterEntityL1, on_delete=models.PROTECT)


class HistoricalInterEntity(InterEntityAbstract, ArchivedModel):
    l2_value = models.CharField(
        "ORACLE - Inter Entity Code",
        max_length=10,
    )
    l1_value = models.CharField(
        "Government Body",
        max_length=10,
    )
    l1_description = models.CharField(
        "Government Body Description",
        max_length=100,
    )
    active = models.BooleanField(default=False)

    def __str__(self):
        s = super().__str__()
        return s + " " + self.financial_year.financial_year_display

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        obj_hist = cls(
            l2_value=obj.l2_value,
            l2_description=obj.l2_description + suffix,
            cpid=obj.cpid,
            l1_description=obj.l1_value.l1_description,
            l1_value=obj.l1_value.l1_value,
            active=obj.active,
            financial_year=year_obj,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Historic Inter-Entity"
        verbose_name_plural = "Historic Inter-Entities"
        ordering = ["financial_year", "l2_value"]


class ProjectCodeAbstract(models.Model):
    project_code = models.CharField(
        "Project Code",
        primary_key=True,
        max_length=50,
    )
    project_description = models.CharField(
        max_length=300, verbose_name="Project Description"
    )

    def __str__(self):
        return self.project_code + " - " + self.project_description

    class Meta:
        abstract = True
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["project_code"]


class ProjectCode(ProjectCodeAbstract, TimeStampedModel, LogChangeModel):
    pass


class HistoricalProjectCode(ProjectCodeAbstract, ArchivedModel):
    project_code = models.CharField("Project Code", max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(
            super().__str__(),
            self.financial_year.financial_year_display,
        )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        obj_hist = cls(
            project_description=obj.project_description + suffix,
            project_code=obj.project_code,
            active=obj.active,
            financial_year=year_obj,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Historic Project"
        verbose_name_plural = "Historic Projects"
        ordering = ["financial_year", "project_code"]


class FCOMappingAbstract(models.Model):
    fco_code = models.IntegerField(
        primary_key=True,
        verbose_name="FCO (Prism) Code",
    )
    fco_description = models.CharField(
        max_length=300, verbose_name="FCO (Prism) Description"
    )

    def __str__(self):
        return str(self.fco_code) + " - " + self.fco_description

    class Meta:
        abstract = True
        verbose_name = "FCO Mapping"
        verbose_name_plural = "FCO Mappings"
        ordering = ["fco_code"]


class FCOMapping(FCOMappingAbstract, TimeStampedModel, LogChangeModel):
    account_L6_code_fk = models.ForeignKey(
        NaturalCode, on_delete=models.PROTECT, blank=True, null=True
    )


class HistoricalFCOMapping(FCOMappingAbstract, ArchivedModel):
    fco_code = models.IntegerField(verbose_name="FCO (Prism) Code")
    account_L6_code = models.IntegerField(
        verbose_name="Oracle (DIT) Code",
    )
    account_L6_description = models.CharField(
        max_length=200,
        verbose_name="Oracle (DIT) Description",
    )
    nac_category_description = models.CharField(
        max_length=200,
        verbose_name="Budget Grouping",
        blank=True,
        null=True,
    )
    budget_description = models.CharField(
        max_length=200,
        verbose_name="Budget Category",
        blank=True,
        null=True,
    )
    economic_budget_code = models.CharField(
        max_length=200, verbose_name="Expenditure Type"
    )

    active = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(
            super().__str__(),
            self.financial_year.financial_year_display,
        )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        if obj.account_L6_code_fk.expenditure_category:
            category = (
                obj.account_L6_code_fk.expenditure_category.NAC_category.NAC_category_description # noqa
            )
            budget_desc = (
                obj.account_L6_code_fk.expenditure_category.grouping_description
            )
        else:
            category = None
            budget_desc = None
        obj_hist = cls(
            fco_description=obj.fco_description + suffix,
            fco_code=obj.fco_code,
            account_L6_code=obj.account_L6_code_fk.natural_account_code,
            account_L6_description=obj.account_L6_code_fk.natural_account_code_description, # noqa
            nac_category_description=category,
            budget_description=budget_desc,
            economic_budget_code=obj.account_L6_code_fk.economic_budget_code,
            active=obj.active,
            financial_year=year_obj,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Historic FCO Mapping"
        verbose_name_plural = "Historic FCO Mappings"
        ordering = ["financial_year", "fco_code"]
