from django.db import models

from core.metamodels import LogChangeModel, TimeStampedModel



# HOSPITALITY, Breakfast
# HOSPITALITY, Lunch
# HOSPITALITY, Dinner (Private)
# HOSPITALITY, Dinner (Public)
# HOSPITALITY, Reception
# GIFT, Gifts
# HOSPITALITY, Sporting/Cultural Event
# HOSPITALITY, Hotel
# HOSPITALITY, Transport
# HOSPITALITY, Air Miles
# HOSPITALITY, Drinks
# HOSPITALITY, Other Hospitality

class GiftAndHospitalityClassification(TimeStampedModel, LogChangeModel):
    GIFT = 'GIFT'
    HOSPITALITY = 'HOSPITALITY'
    GF_TYPE = (
        (GIFT, 'Gift'),
        (HOSPITALITY, 'Hospitality'))

    gift_type = models.CharField(max_length=20,
                                    choices=GF_TYPE, default=HOSPITALITY,
                                    verbose_name='Type')
    gif_hospitality_classification = models.CharField(max_length=100)

    def __str__(self):
        return str(self.gift_type) + ' - ' + str(self.gif_hospitality_classification)

    class Meta:
        verbose_name = "Gift and Hospitality Classification"
        verbose_name_plural = "Gift and Hospitality Classifications"
        ordering = ['gif_hospitality_classification']



class GiftAndHospitalityCategory(TimeStampedModel, LogChangeModel):
    gif_hospitality_category = models.CharField(max_length=100)

    def __str__(self):
        return str(self.gif_hospitality_category)

    class Meta:
        verbose_name = "Gift and Hospitality Category"
        verbose_name_plural = "Gift and Hospitality Categories"
        ordering = ['gif_hospitality_category']


class GiftAndHospitalityCompany(TimeStampedModel, LogChangeModel):
    gif_hospitality_company = models.CharField(max_length=100)

    def __str__(self):
        return str(self.gif_hospitality_company)

    class Meta:
        verbose_name = "Gift and Hospitality Company"
        verbose_name_plural = "Gift and Hospitality Companies"
        ordering = ['gif_hospitality_company']

    # Gift and Hospitality
class GiftAndHospitality(LogChangeModel):
    """Model used to keep information of gifts/hospitality received/offered by DIT people.
    On purpose, I am not using foreign key anywhere, because we need to have a record of details
    when the gift was registered, not later on."""
    id = models.AutoField('Record ID', primary_key=True)
    classification_fk = models.ForeignKey('GiftAndHospitalityClassification',
                                          on_delete= models.SET_NULL,
                                          null=True, blank=True)
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
    company_fk = models.ForeignKey('GiftAndHospitalityCompany',
                                          on_delete= models.SET_NULL,
                                          null=True, blank=True)
    company = models.CharField(max_length=100)
    ACTION_TYPE = (
        ('Action1', 'Accepted'),
        ('Action2', 'Accepted (difference paid to Department)'),
        ('Action3', 'Accepted (surrendered to Department)'),
    )
    action_taken = models.CharField(max_length=20,
                                    choices=ACTION_TYPE,
                                    verbose_name='Action taken')
    entered_by = models.CharField(max_length=50)
    staff_no = models.CharField(max_length=50)
    entered_date_stamp = models.DateTimeField(auto_now=True)
    category_fk = models.ForeignKey('GiftAndHospitalityCategory',
                                          on_delete= models.SET_NULL,
                                          null=True, blank=True)
    category = models.CharField(max_length=100)
    # Copy the grade, in case grades changes in future, even if unlikely

    grade = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Gift and Hospitality"
        verbose_name_plural = "Gift and Hospitality"

