from django.db import models

from core.metamodels import TimeStampedModel

class GiftsAndHospitalityClassification(TimeStampedModel):
    GIFT = 'GIFT'
    HOSPITALITY = 'HOSPITALITY'
    GF_TYPE = (
        (GIFT, 'Gift'),
        (HOSPITALITY, 'Hospitality'))

    gift_type = models.CharField(max_length=20,
                                    choices=GF_TYPE, default=HOSPITALITY,
                                    verbose_name='Type')
    classification = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Gift and Hospitality Classification"
        verbose_name_plural = "Gifts and Hospitality Classifications"


class GiftsAndHospitalityCategory(TimeStampedModel):
    category = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Gifts and Hospitality Category"
        verbose_name_plural = "Gifts and Hospitality Categories"



class GiftsAndHospitalityCompany(TimeStampedModel):
    company = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Gifts and Hospitality Company"
        verbose_name_plural = "Gifts and Hospitality Companies"


    # Gift and Hospitality
class GiftsAndHospitality(models.Model):
    """Model used to keep information of gifts/hospitality received/offered by DIT people.
    On purpose, I am not using foreign key anywhere, because we need to have a record of details
    when the gift was registered, not later on."""
    classification = models.CharField(max_length=100)
    group_name = models.CharField(max_length=200)
    date_offered = models.DateField()
    venue = models.CharField(max_length=1000)
    reason = models.CharField(max_length=1000)
    value = models.DecimalField(max_digits=18, decimal_places=2)
    band = models.CharField(max_length=50)
    rep = models.CharField(max_length=255)
    OFFER_CHOICE =(
        ('Received', 'Received'),
        ('Offered', 'Offered')
    )
    offer = models.CharField(max_length=50, choices=OFFER_CHOICE)
    company_rep = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    ACTION_TYPE = (
        ('Action1', 'Accepted'),
        ('Action2', 'Accepted (difference paid to Department)'),
        ('Action3', 'Accepted (surrendered to Department)'),
    )
    action_taken = models.CharField(max_length=20,
                                    choices=ACTION_TYPE,
                                    verbose_name='Action taken')
    date_stamp = models.DateTimeField()
    entered_by = models.CharField(max_length=50)
    staff_no = models.CharField(max_length=50)
    entered_date_stamp = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100)
    # Copy the grade, in case grades changes in future, even if unlikely
    grade = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Gifts and Hospitality"
        verbose_name_plural = "Gifts and Hospitality"

