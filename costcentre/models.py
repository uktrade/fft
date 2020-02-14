from django.db import models

from core.metamodels import (
    ArchivedModel,
    IsActiveModel,
)

from treasurySS.models import Segment


class CostCentrePerson(IsActiveModel):
    """Model used for storing the name of Deputy Directors, Directors and DG.
    It would be better to use the  HR data, but they are not always up-to-date,
    so it is easier to have a different table."""

    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100)
    email = models.EmailField("Email", null=True, blank=True)
    is_director = models.BooleanField("Director", default=False)
    is_dg = models.BooleanField("General Director", default=False)

    def _get_full_name(self):
        "Returns the person's full name."
        return "%s %s" % (self.surname, self.name)

    full_name = property(_get_full_name)

    def __str__(self):
        return str(self.name) + " " + str(self.surname)

    class Meta:
        verbose_name = "Hierarchy Responsibility"
        verbose_name_plural = "Hierarchy Responsibilities"
        ordering = ["surname", "name"]


class BusinessPartner(IsActiveModel):
    """Model used for storing information about the business partners"""

    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100)
    bp_email = models.EmailField("Business Partner email", null=True, blank=True)

    def __str__(self):
        return str(self.name) + " " + str(self.surname)

    class Meta:
        verbose_name = "Business Partner"
        verbose_name_plural = "Business Partners"
        ordering = ["surname", "name"]


class BSCEEmail(IsActiveModel):
    """Model used to store the generic BSCE email"""

    bsce_email = models.EmailField("BSCE email", unique=True)

    def __str__(self):
        return str(self.bsce_email)

    class Meta:
        verbose_name = "BSCE Email"
        verbose_name_plural = "BSCE Emails"
        ordering = ["bsce_email"]


class DepartmentalGroup(IsActiveModel):
    group_code = models.CharField("Group Code", primary_key=True, max_length=6)
    group_name = models.CharField("Group Name", max_length=300)
    director_general = models.ForeignKey(
        CostCentrePerson, on_delete=models.PROTECT, null=True, blank=True
    )
    treasury_segment_fk = models.ForeignKey(
        Segment,
        verbose_name="Treasury Segment",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.group_name)

    class Meta:
        verbose_name = "Departmental Group"
        verbose_name_plural = "Departmental Groups"
        ordering = ["group_code"]


class Directorate(IsActiveModel):
    directorate_code = models.CharField(
        "Directorate Code", primary_key=True, max_length=6
    )
    directorate_name = models.CharField("Directorate Name", max_length=300)
    director = models.ForeignKey(
        "CostCentrePerson", on_delete=models.PROTECT, null=True, blank=True
    )
    group = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.directorate_name)

    class Meta:
        verbose_name = "Directorate"
        verbose_name_plural = "Directorates"
        ordering = ["directorate_code"]


class CostCentre(IsActiveModel):
    cost_centre_code = models.CharField(
        "Cost Centre Code", primary_key=True, max_length=6
    )
    cost_centre_name = models.CharField("Cost Centre Name", max_length=300)
    directorate = models.ForeignKey(Directorate, on_delete=models.PROTECT)
    deputy_director = models.ForeignKey(
        CostCentrePerson,
        on_delete=models.PROTECT,
        verbose_name="Deputy Director",
        null=True,
        blank=True,
    )
    business_partner = models.ForeignKey(
        "BusinessPartner",
        verbose_name="Finance Business Partner",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    bsce_email = models.ForeignKey(
        BSCEEmail,
        verbose_name="BSCE Email",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    disabled_with_actual = models.BooleanField(
        "Disabled (Actuals to be cleared)", default="False"
    )
    used_for_travel = models.BooleanField("Used for Travel", default="True")

    @property
    def full_name(self):
        return "{} - {}".format(
            self.cost_centre_code,
            self.cost_centre_name,
        )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Cost Centre"
        verbose_name_plural = "Cost Centres"
        ordering = ["cost_centre_code"]


class HistoricCostCentre(ArchivedModel):
    """Repository for historical cost centres hierarchies.
    The table is not normalised, to make life easier when retrieving data"""

    group_code = models.CharField("Group Code", max_length=50)
    group_name = models.CharField("Group Name", max_length=300)
    dg_fullname = models.CharField(
        "Director General", max_length=200, null=True, blank=True
    )
    directorate_code = models.CharField("Directorate Code", max_length=50)
    directorate_name = models.CharField("Directorate Name", max_length=300)
    director_fullname = models.CharField(
        "Director", max_length=200, null=True, blank=True
    )
    cost_centre_code = models.CharField("Cost Centre Code", max_length=50)
    cost_centre_name = models.CharField("Cost Centre Name", max_length=300)
    deputy_director_fullname = models.CharField(
        "Deputy Director", max_length=200, null=True, blank=True
    )
    business_partner_fullname = models.CharField(
        "Business Partner", max_length=200, null=True, blank=True
    )
    bsce_email = models.ForeignKey(
        BSCEEmail,
        verbose_name="BSCE Email",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    active = models.BooleanField(default="True")
    disabled_with_actual = models.BooleanField(
        "Disabled (Actuals to be cleared)", default="False"
    )

    @classmethod
    def archive_year(cls, cc_obj, year_obj, suffix=""):
        cc_hist = cls(
            group_code=cc_obj.directorate.group.group_code,
            group_name=cc_obj.directorate.group.group_name + suffix,
            dg_fullname=cc_obj.directorate.group.director_general,
            directorate_code=cc_obj.directorate.directorate_code,
            directorate_name=cc_obj.directorate.directorate_name + suffix,
            director_fullname=cc_obj.directorate.director,
            cost_centre_code=cc_obj.cost_centre_code,
            cost_centre_name=cc_obj.cost_centre_name + suffix,
            deputy_director_fullname=cc_obj.deputy_director,
            business_partner_fullname=cc_obj.business_partner,
            financial_year=year_obj,
            bsce_email=cc_obj.bsce_email,
            active=cc_obj.active,
            disabled_with_actual=cc_obj.disabled_with_actual,
        )
        cc_hist.save()
        return cc_hist

    def __str__(self):
        return (
            str(self.cost_centre_code)
            + " - "
            + str(self.cost_centre_name)
            + " "
            + self.financial_year.financial_year_display
        )

    class Meta:
        verbose_name = "Historic Cost Centre"
        verbose_name_plural = "Historic Cost Centres"
        ordering = ["cost_centre_code"]
        unique_together = ("cost_centre_code", "financial_year")
