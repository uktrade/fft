from django.db import models

from core.metamodels import ArchivedModel, BaseModel, IsActiveModel
from treasuryCOA.models import L5Account


# Other members of Account Codes
class Analysis1Abstract(models.Model):
    analysis1_code = models.CharField("Contract Code", primary_key=True, max_length=50,)
    analysis1_description = models.CharField("Contract Name", max_length=300,)
    supplier = models.CharField(
        "Supplier", max_length=300, default="", blank=True, null=True,
    )
    pc_reference = models.CharField(
        "PC Reference", max_length=300, default="", blank=True, null=True,
    )

    def __str__(self):
        return "{} - {}".format(self.analysis1_code, self.analysis1_description,)

    class Meta:
        abstract = True
        verbose_name_plural = "Contract Reconciliations (Analysis 1)"
        verbose_name = "Contract Reconciliation (Analysis 1)"
        ordering = ["analysis1_code"]


class Analysis1(Analysis1Abstract, IsActiveModel):
    pass


class ArchivedAnalysis1(Analysis1Abstract, ArchivedModel):
    analysis1_code = models.CharField("Contract Code", max_length=50)
    active = models.BooleanField(default=True)
    chart_of_account_code_name = "analysis1_code"

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
        verbose_name_plural = "Archived Contract Reconciliations (Analysis 1)"
        verbose_name = "Archived Contract Reconciliation (Analysis 1)"
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


class Analysis2(Analysis2Abstract, IsActiveModel):
    pass


class ArchivedAnalysis2(Analysis2Abstract, ArchivedModel):
    analysis2_code = models.CharField("Contract Code", max_length=50)
    active = models.BooleanField(default=True)
    chart_of_account_code_name = "analysis2_code"

    def __str__(self):
        return "{} {}".format(
            super().__str__(), self.financial_year.financial_year_display,
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
        verbose_name = "Archived Market (Analysis 2)"
        verbose_name_plural = "Archived Markets (Analysis 2)"
        ordering = ["financial_year", "analysis2_code"]


# Category defined by DBT
class NACCategory(IsActiveModel):
    NAC_category_description = models.CharField(
        max_length=255, verbose_name="Budget Grouping", unique=True
    )
    PAY = "P"
    NON_PAY = "NP"

    PAY_NONPAY_CHOICE = [
        (PAY, "Pay"),
        (NON_PAY, "Non Pay"),
    ]
    # At the moment, the following field is derived from the description
    # I decided to create a new field, in case the rule will change in the future.
    # It is not a big deal to create the extra field!
    pay_nonpay = models.CharField(
        max_length=20,
        choices=PAY_NONPAY_CHOICE,
        default=NON_PAY
    )
    NAC_category_display_order = models.IntegerField(blank=True, null=True,)

    def __str__(self):
        return str(self.NAC_category_description)

    class Meta:
        verbose_name = "Budget Grouping"
        verbose_name_plural = "Budget Groupings"
        ordering = ["NAC_category_display_order"]


class OperatingDeliveryCategory(IsActiveModel):
    """Another way to classify the Budget NACs"""

    operating_delivery_description = models.CharField(
        max_length=255, verbose_name="Operating Delivery Plan Category", unique=True,
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
    further_description = models.CharField(max_length=5000, blank=True, null=True,)
    NAC_category = models.ForeignKey(
        NACCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Budget Grouping",
    )
    # Introduced to fix the ordering on view forecast
    expenditurecategory_display_order = models.IntegerField(
        blank=True, null=True, default=99
    )

    def __str__(self):
        return str(self.grouping_description)

    class Meta:
        abstract = True
        verbose_name = "Budget Category"
        verbose_name_plural = "Budget Categories"
        ordering = ["expenditurecategory_display_order"]


class ExpenditureCategory(
    ExpenditureCategoryAbstract, IsActiveModel,
):
    linked_budget_code = models.ForeignKey(
        "NaturalCode",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Budget Code",
    )
    op_del_category = models.ForeignKey(
        OperatingDeliveryCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Operating Delivery Plan",
    )


class ArchivedExpenditureCategory(
    ExpenditureCategoryAbstract, ArchivedModel,
):
    grouping_description = models.CharField(
        max_length=255, verbose_name="Budget Category", unique=False
    )
    linked_budget_code = models.IntegerField(
        verbose_name="Budget Code", blank=True, null=True,
    )
    linked_budget_code_description = models.CharField(
        max_length=200, verbose_name="Budget Description", blank=True, null=True,
    )
    NAC_category_description = models.CharField(
        max_length=255, verbose_name="Budget Grouping", blank=True, null=True,
    )
    NAC_pay_non_pay = models.CharField(
        max_length=255, verbose_name="Pay Non-Pay", blank=True, null=True,
    )
    active = models.BooleanField(default=True)
    chart_of_account_code_name = "grouping_description"

    def __str__(self):
        return "{} {}".format(
            super().__str__(), self.financial_year.financial_year_display,
        )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        obj_hist = cls(
            financial_year=year_obj,
            active=obj.active,
            grouping_description=obj.grouping_description + suffix,
            NAC_category=obj.NAC_category,
            NAC_category_description=obj.NAC_category.NAC_category_description
            if obj.NAC_category
            else None,
            NAC_pay_non_pay=obj.NAC_category.pay_nonpay
            if obj.NAC_category
            else None,
            description=obj.description,
            further_description=obj.further_description,
            linked_budget_code=obj.linked_budget_code.natural_account_code
            if obj.linked_budget_code
            else None,
            linked_budget_code_description=obj.linked_budget_code.natural_account_code_description  # noqa
            if obj.linked_budget_code
            else None,
            expenditurecategory_display_order=obj.expenditurecategory_display_order,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Archived Budget Category"
        verbose_name_plural = "Archived Budget Categories"
        ordering = ["financial_year", "expenditurecategory_display_order"]


class CommercialCategoryAbstract(models.Model):
    commercial_category = models.CharField(
        max_length=255, verbose_name="Commercial Category", unique=True,
    )
    description = models.CharField(max_length=5000, blank=True, null=True,)
    approvers = models.CharField(max_length=5000, blank=True, null=True,)

    def __str__(self):
        return str(self.commercial_category)

    class Meta:
        abstract = True
        verbose_name = "Commercial Category"
        verbose_name_plural = "Commercial Categories"
        ordering = ["commercial_category"]


class CommercialCategory(
    CommercialCategoryAbstract, IsActiveModel,
):
    pass


class ArchivedCommercialCategory(
    CommercialCategoryAbstract, ArchivedModel,
):
    commercial_category = models.CharField(
        max_length=255, verbose_name="Commercial Category", unique=False,
    )

    active = models.BooleanField(default=True)
    chart_of_account_code_name = "commercial_category"

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
        verbose_name = "Archived Commercial Category"
        verbose_name_plural = "Archived Commercial Categories"
        ordering = ["financial_year", "commercial_category"]


# define level1 values: Capital, staff, etc is Level 1 in UKTI nac hierarchy
class NaturalCodeAbstract(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Natural Account Code (NAC)"
        verbose_name_plural = "Natural Account Codes (NAC)"
        ordering = ["natural_account_code"]

    natural_account_code = models.IntegerField(primary_key=True, verbose_name="NAC",)
    natural_account_code_description = models.CharField(
        max_length=200, verbose_name="NAC Description"
    )
    used_for_budget = models.BooleanField(default=False)

    economic_budget_code = models.CharField(
        max_length=255, verbose_name="Expenditure Type", blank=True, null=True,
    )
    GROSS = "GR"
    INCOME = "IN"
    GROSS_INCOME_CHOICE = [
        (GROSS, "Gross"),
        (INCOME, "Income")
    ]
    gross_income = models.CharField(
        max_length=20,
        choices=GROSS_INCOME_CHOICE,
        blank=True,
        null=True,
    )
    CASH = "CH"
    NON_CASH = "NC"
    NOT_DEFINED = "NA"

    CASH_NONCASH_CHOICE = [
        (CASH, "Cash"),
        (NON_CASH, "Non-Cash"),
        (NOT_DEFINED, "N/A Cash")
    ]
    cash_non_cash = models.CharField(
        max_length=20,
        choices=CASH_NONCASH_CHOICE,
        default=NOT_DEFINED
    )

    def __str__(self):
        return "{} - {}".format(
            self.natural_account_code, self.natural_account_code_description
        )


class NaturalCode(NaturalCodeAbstract, IsActiveModel):
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
            l5_linked = L5Account.objects.get(account_l5_code=link_l5_code,)
            self.economic_budget_code = l5_linked.economic_budget_code
        super(NaturalCode, self).save(*args, **kwargs)


class ArchivedNaturalCode(NaturalCodeAbstract, ArchivedModel):
    """It includes the fields displayed on the FIDO interface,
    and it has no foreign keys in it, to avoid dependencies
    from other tables. The table is not normalised by design."""

    natural_account_code = models.IntegerField(verbose_name="PO/Actuals NAC")
    expenditure_category = models.ForeignKey(
        ArchivedExpenditureCategory,
        verbose_name="Budget Category",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    expenditure_category_description = models.CharField(
        max_length=255, verbose_name="Budget Category", blank=True, null=True
    )
    NAC_category = models.CharField(
        max_length=255, verbose_name="Budget Grouping", blank=True, null=True
    )
    NAC_pay_non_pay = models.CharField(
        max_length=255, verbose_name="Pay Non-Pay", blank=True, null=True,
    )
    commercial_category = models.CharField(
        max_length=255, verbose_name="Commercial Category", blank=True, null=True
    )
    account_L5_code = models.BigIntegerField(blank=True, null=True)
    account_L5_description = models.CharField(max_length=255, blank=True, null=True,)
    account_L6_budget = models.BigIntegerField(
        "Budget/Forecast NAC", blank=True, null=True
    )
    account_L5_code_upload = models.BigIntegerField(
        verbose_name="L5 for OSCAR upload", blank=True, null=True
    )
    op_delivery_plan = models.CharField(
        max_length=255, verbose_name="Operational Delivery Plan",
        blank=True,
        null=True
    )
    active = models.BooleanField(default=True)
    chart_of_account_code_name = "natural_account_code"

    def __str__(self):
        return super().__str__() + " " + self.financial_year.financial_year_display

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        op_delivery_plan_value = None
        if obj.expenditure_category:
            expenditure_category_value = obj.expenditure_category.grouping_description
            # Find the archived equivalent
            expenditure_category_obj = ArchivedExpenditureCategory.objects.get(
                grouping_description=obj.expenditure_category.grouping_description,
                financial_year=year_obj,
            )
            expenditure_category_id = expenditure_category_obj.id

            NAC_category_value = (
                obj.expenditure_category.NAC_category.NAC_category_description
            )
            pay_non_pay_value = obj.expenditure_category.NAC_category.pay_nonpay
            account_L6_budget_value = (
                obj.expenditure_category.linked_budget_code.natural_account_code
            )
            if obj.expenditure_category.op_del_category:
                op_delivery_plan_value = obj.expenditure_category.\
                    op_del_category.operating_delivery_description
        else:
            expenditure_category_id = None
            expenditure_category_value = None
            NAC_category_value = None
            account_L6_budget_value = None
            pay_non_pay_value = None

        if obj.commercial_category:
            commercial_category_value = obj.commercial_category.commercial_category
        else:
            commercial_category_value = None
        if obj.account_L5_code_upload:
            account_L5_code_upload_value = obj.account_L5_code_upload.account_l5_code
        else:
            account_L5_code_upload_value = None
        if obj.account_L5_code:
            account_L5_code_value = obj.account_L5_code.account_l5_code
            account_L5_description_value = obj.account_L5_code.account_l5_long_name
        else:
            account_L5_code_value = None
            account_L5_description_value = None
        obj_hist = cls(
            natural_account_code_description=obj.natural_account_code_description
            + suffix,  # noqa
            natural_account_code=obj.natural_account_code,
            used_for_budget=obj.used_for_budget,
            expenditure_category_id=expenditure_category_id,
            expenditure_category_description=expenditure_category_value,
            NAC_category=NAC_category_value,
            commercial_category=commercial_category_value,
            account_L6_budget=account_L6_budget_value,
            account_L5_code=account_L5_code_value,
            account_L5_description=account_L5_description_value,
            account_L5_code_upload=account_L5_code_upload_value,
            economic_budget_code=obj.economic_budget_code,
            op_delivery_plan=op_delivery_plan_value,
            gross_income=obj.gross_income,
            cash_non_cash=obj.cash_non_cash,
            NAC_pay_non_pay=pay_non_pay_value,
            financial_year=year_obj,
            active=obj.active,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Archived Natural Account Code (NAC)"
        verbose_name_plural = "Archived Natural Account Codes (NAC)"
        ordering = ["financial_year", "natural_account_code"]


class BudgetType(BaseModel):
    budget_type_key = models.CharField("Key", primary_key=True, max_length=50)
    budget_type = models.CharField("Budget Type", max_length=100)
    # budget_type_display is used when showing the forecast view
    budget_type_display = models.CharField(max_length=100, blank=True, null=True)
    budget_type_display_order = models.IntegerField(default=99)
    budget_type_edit_display_order = models.IntegerField(default=99)

    def __str__(self):
        return self.budget_type


class ProgrammeCodeAbstract(models.Model):
    programme_code = models.CharField(
        "Programme Code", primary_key=True, max_length=50,
    )
    programme_description = models.CharField("Programme Name", max_length=100,)
    budget_type = models.ForeignKey(
        BudgetType,
        verbose_name="Budget Type",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s",
    )

    def __str__(self):
        return self.programme_code + " - " + self.programme_description

    class Meta:
        abstract = True
        verbose_name = "Programme Code"
        verbose_name_plural = "Programme Codes"
        ordering = ["programme_code"]


class ProgrammeCode(ProgrammeCodeAbstract, IsActiveModel):
    pass


class ArchivedProgrammeCode(ProgrammeCodeAbstract, ArchivedModel):
    programme_code = models.CharField("Programme Code", max_length=50)
    active = models.BooleanField(default=True)
    chart_of_account_code_name = "programme_code"

    def __str__(self):
        s = super().__str__()
        return s + " " + self.financial_year.financial_year_display

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        pc_hist = cls(
            programme_code=obj.programme_code,
            programme_description="{}{}".format(obj.programme_description, suffix,),
            budget_type=obj.budget_type,
            active=obj.active,
            financial_year=year_obj,
        )
        pc_hist.save()
        return pc_hist

    class Meta:
        verbose_name = "Archived Programme Code"
        verbose_name_plural = "Archived Programme Codes"
        ordering = ["financial_year", "programme_code"]


class InterEntityL1(IsActiveModel):
    l1_value = models.CharField("Government Body", primary_key=True, max_length=10,)
    l1_description = models.CharField("Government Body Description", max_length=100,)

    def __str__(self):
        return self.l1_value + " - " + self.l1_description

    class Meta:
        verbose_name = "Government Body"
        verbose_name_plural = "Government Bodies"
        ordering = ["l1_value"]


class InterEntityAbstract(models.Model):
    l2_value = models.CharField(
        "ORACLE - Inter Entity Code", primary_key=True, max_length=10,
    )
    l2_description = models.CharField(
        "ORACLE - Inter Entity Description", max_length=100,
    )
    cpid = models.CharField("Treasury - CPID (Departmental Code No.)", max_length=10,)

    def __str__(self):
        return self.l2_value + " - " + self.l2_description

    class Meta:
        abstract = True
        verbose_name = "Inter-Entity"
        verbose_name_plural = "Inter-Entities"
        ordering = ["l2_value"]


class InterEntity(InterEntityAbstract, IsActiveModel):
    l1_value = models.ForeignKey(InterEntityL1, on_delete=models.PROTECT)


class ArchivedInterEntity(InterEntityAbstract, ArchivedModel):
    l2_value = models.CharField("ORACLE - Inter Entity Code", max_length=10,)
    l1_value = models.CharField("Government Body", max_length=10,)
    l1_description = models.CharField("Government Body Description", max_length=100,)
    active = models.BooleanField(default=True)
    chart_of_account_code_name = "l2_value"

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
        verbose_name = "Archived Inter-Entity"
        verbose_name_plural = "Archived Inter-Entities"
        ordering = ["financial_year", "l2_value"]


class ProjectCodeAbstract(models.Model):
    project_code = models.CharField("Project Code", primary_key=True, max_length=50,)
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


class ProjectCode(ProjectCodeAbstract, IsActiveModel):
    pass


class ArchivedProjectCode(ProjectCodeAbstract, ArchivedModel):
    project_code = models.CharField("Project Code", max_length=50)
    active = models.BooleanField(default=True)
    chart_of_account_code_name = "project_code"

    def __str__(self):
        return "{} {}".format(
            super().__str__(), self.financial_year.financial_year_display,
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
        verbose_name = "Archived Project"
        verbose_name_plural = "Archived Projects"
        ordering = ["financial_year", "project_code"]


class FCOMappingAbstract(models.Model):
    fco_code = models.IntegerField(primary_key=True, verbose_name="FCO (Prism) Code",)
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


class FCOMapping(FCOMappingAbstract, IsActiveModel):
    account_L6_code_fk = models.ForeignKey(
        NaturalCode, on_delete=models.PROTECT, blank=True, null=True
    )


class ArchivedFCOMapping(FCOMappingAbstract, ArchivedModel):
    fco_code = models.IntegerField(verbose_name="FCO (Prism) Code")
    account_L6_code = models.IntegerField(verbose_name="Oracle (DBT) Code",)
    account_L6_description = models.CharField(
        max_length=200, verbose_name="Oracle (DBT) Description",
    )
    nac_category_description = models.CharField(
        max_length=200, verbose_name="Budget Grouping", blank=True, null=True,
    )
    budget_description = models.CharField(
        max_length=200, verbose_name="Budget Category", blank=True, null=True,
    )
    economic_budget_code = models.CharField(
        max_length=200, verbose_name="Expenditure Type"
    )

    active = models.BooleanField(default=True)
    chart_of_account_code_name = "fco_code"

    def __str__(self):
        return "{} {}".format(
            super().__str__(), self.financial_year.financial_year_display,
        )

    @classmethod
    def archive_year(cls, obj, year_obj, suffix=""):
        if obj.account_L6_code_fk.expenditure_category:
            category = (
                obj.account_L6_code_fk.expenditure_category.NAC_category.NAC_category_description  # noqa
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
            account_L6_description=obj.account_L6_code_fk.natural_account_code_description,  # noqa
            nac_category_description=category,
            budget_description=budget_desc,
            economic_budget_code=obj.account_L6_code_fk.economic_budget_code,
            active=obj.active,
            financial_year=year_obj,
        )
        obj_hist.save()
        return obj_hist

    class Meta:
        verbose_name = "Archived FCO Mapping"
        verbose_name_plural = "Archived FCO Mappings"
        ordering = ["financial_year", "fco_code"]
