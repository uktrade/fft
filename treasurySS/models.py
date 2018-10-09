from core.metamodels import TimeStampedModel

from django.db import models


# Treasury data
class SegmentGrandParent(TimeStampedModel):
    segment_grand_parent_code = models.CharField(max_length=8, primary_key=True,
                                                 verbose_name='segment grand parent code')
    segment_grand_parent_long_name = models.CharField(max_length=255,
                                                      verbose_name='segment grandparent long name')

    def __str__(self):
        return self.Segment_grand_parent_code


class SegmentParent(TimeStampedModel):
    segment_parent_code = models.CharField(max_length=8, primary_key=True,
                                           verbose_name='segment parent code')
    segment_parent_long_name = models.CharField(max_length=255,
                                                verbose_name='segment parent long name')
    segment_grand_parent_code = models.ForeignKey(SegmentGrandParent, on_delete=models.PROTECT)

    def __str__(self):
        return self.Segment_parent_code


class Segment(TimeStampedModel):
    segment_code = models.CharField(max_length=8, primary_key=True, verbose_name='segment code')
    segment_long_name = models.CharField(max_length=255, verbose_name='segment long name')
    segment_parent_code = models.ForeignKey(SegmentParent, on_delete=models.PROTECT)

    def __str__(self):
        return self.segment_code


class EstimateRow(TimeStampedModel):
    estimate_row_code = models.CharField(max_length=8, primary_key=True,
                                         verbose_name='estimates row code')
    estimate_row_long_name = models.CharField(max_length=255,
                                              verbose_name='estimates row long name')

    def __str__(self):
        return self.estimate_row_code


class SubSegment(TimeStampedModel):
    VOTED = 'VT'
    NON_VOTED = 'NVT'
    UNDEF = 'N/A'
    CONTROL_ACCOUNTING_AUTH_CHOICES = (
        (VOTED, 'VOTED'),
        (NON_VOTED, (('NON - VOTED_DEPT', 'NON - VOTED_DEPT'),
                     ('NON-VOTED_CFER', 'NON-VOTED_CFER'),
                     ('NON-VOTED_CF', 'NON-VOTED_CF'),
                     ('NON-VOTED_PC', 'NON-VOTED_PC'),
                     ('NON-VOTED_NIF', 'NON-VOTED_NIF'),
                     ('NON-VOTED_NLF', 'NON-VOTED_NLF'),
                     ('NON-VOTED_CEX', 'NON-VOTED_CEX'),
                     ('NON-VOTED_SF', 'NON-VOTED_SF'),
                     ('NON-VOTED_LG', 'NON-VOTED_LG'),
                     ('NON-VOTED_DA', 'NON-VOTED_DA'),)),
        (UNDEF, UNDEF),
    )

    DEL = 'DEL'
    AME = 'AME'
    NB = 'NON-BUDGET'
    DELADM = 'DEL ADMIN'
    DELPROG = 'DEL PROG'
    AMEDEPT = 'DEPT AME'
    AMENODEPT = 'NON-DEPT AME'
    CONTROL_BUDGET_CHOICES = {
        (DEL, ((DELADM, 'DEL ADMIN'), (DELPROG, 'DEL PROG'),)),
        (AME, ((AMEDEPT, 'DEPT AME'), (AMENODEPT, 'NON-DEPT AME'),)),
        (NB, NB),
    }
    sub_segment_code = models.CharField(max_length=8, primary_key=True,
                                        verbose_name='sub segment code')
    sub_segment_long_name = models.CharField(max_length=255, verbose_name='sub segment long name')
    Segment_code = models.ForeignKey(Segment, on_delete=models.PROTECT)
    control_budget_detail_code = models.CharField(max_length=50,
                                                  choices=CONTROL_BUDGET_CHOICES, default=NB,
                                                  verbose_name='control budget detail code')
    estimates_row_code = models.ForeignKey(EstimateRow, on_delete=models.PROTECT)
    net_subhead_code = models.CharField(max_length=255, verbose_name='net subhead code')
    policy_ringfence_code = models.CharField(max_length=255, verbose_name='policy ringfence code')
    accounting_authority_code = models.CharField(max_length=255,
                                                 verbose_name='accounting authority code')
    accounting_authority_DetailCode = \
        models.CharField(max_length=255,
                         choices=CONTROL_ACCOUNTING_AUTH_CHOICES,
                         default=UNDEF,
                         verbose_name='accounting authority detail code')

    def __str__(self):
        return self.sub_segment_code
