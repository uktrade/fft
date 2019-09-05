from chartofaccountDIT.models import Analysis1, Analysis2, NaturalCode, ProgrammeCode

from core.metamodels import TimeStampedModel

from costcentre.models import CostCentre

from django.db import models

from treasurySS.models import SubSegment


# The ADIReport contains the forecast and the actuals
# The current month defines what is Actual and what is Forecast
class ADIReport(TimeStampedModel):
    financial_year = models.IntegerField()
    programme = models.ForeignKey(ProgrammeCode, on_delete=models.PROTECT)
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    natural_account_code = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
    analysis1_code = models.ForeignKey(Analysis1, on_delete=models.PROTECT)
    analysis2_code = models.ForeignKey(Analysis2, on_delete=models.PROTECT)
    original_budget = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    budget = models.DecimalField(max_digits=18, decimal_places=0, default=0)
    apr = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    may = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    jun = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    jul = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    aug = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    sep = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    oct = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    nov = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dec = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    jan = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    feb = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    mar = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    adj1 = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    adj2 = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    adj3 = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    narrative = models.CharField(max_length=2000, blank=True)
    created_by = models.CharField(max_length=100, blank=True)
    update_by = models.CharField(max_length=100, blank=True)

    @property
    def year_total(self):
        """Returns the total for the year"""
        return self.apr + self.may + self.jun + self.jul + self.aug + self.sep \
            + self.oct + self.nov + self.dec + self.jan + self.feb + self.mar

    class Meta:
        unique_together = ('financial_year',
                           'programme',
                           'cost_centre',
                           'natural_account_code',
                           'analysis1_code',
                           'analysis2_code')

    def __str__(self):
        return str(self.cost_centre) + '--' + str(self.programme) + '--' + str(self.natural_account_code)


# table for
# The sub segment is mapped to the combination of Programme and Cost Centre
class SubSegmentUKTIMapping(TimeStampedModel):
    sub_segment_code = models.ForeignKey(SubSegment, on_delete=models.PROTECT)
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    programme = models.ForeignKey(ProgrammeCode, on_delete=models.PROTECT)
