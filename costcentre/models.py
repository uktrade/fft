from django.db import models

from core.metamodels import LogChangeModel, TimeStampedModel  # noqa I100


class DepartmentalGroup(TimeStampedModel, LogChangeModel):
    group_code = models.CharField('Group No.', primary_key=True, max_length=6)
    group_name = models.CharField('Group Name', max_length=300)
    director_general = models.ForeignKey('payroll.DITPeople', on_delete=models.PROTECT,
                                         null=True, blank=True)

    def __str__(self):
        return str(self.group_name)

    class Meta:
        verbose_name = "Departmental Group"
        verbose_name_plural = "Departmental Groups"


class Directorate(TimeStampedModel, LogChangeModel):
    directorate_code = models.CharField('Directorate', primary_key=True, max_length=6)
    directorate_name = models.CharField('Directorate No.', max_length=300)
    director = models.ForeignKey('payroll.DITPeople', on_delete=models.PROTECT,
                                 null=True, blank=True)
    group = models.ForeignKey(DepartmentalGroup, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.directorate_name)

    class Meta:
        verbose_name = "Directorate"
        verbose_name_plural = "Directorates"


class BSCEEmail(TimeStampedModel, LogChangeModel):
    bsce_email = models.EmailField('BSCE email')

    def __str__(self):
        return str(self.bsce_email)

    class Meta:
        verbose_name = "BSCE Email"
        verbose_name_plural = "BSCE Emails"


class CostCentre(TimeStampedModel, LogChangeModel):
    cost_centre_code = models.CharField('Cost Centre No.', primary_key=True, max_length=6)
    cost_centre_name = models.CharField('Cost Centre Name', max_length=300)
    directorate = models.ForeignKey(Directorate, on_delete=models.PROTECT)
    deputy_director = models.ForeignKey('payroll.DITPeople', on_delete=models.PROTECT,
                                        related_name='deputy_director', null=True, blank=True)
    business_partner = models.ForeignKey('payroll.DITPeople',
                                         verbose_name='Finance Business Partner',
                                         on_delete=models.PROTECT, related_name='business_partner',
                                         null=True, blank=True)
    bsce_email = models.ForeignKey(BSCEEmail, verbose_name='BSCE Email',
                                         on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.cost_centre_code) + ' - ' + str(self.cost_centre_name)

    class Meta:
        verbose_name = "Cost Centre"
        verbose_name_plural = "Cost Centres"


