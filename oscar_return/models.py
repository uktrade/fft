from django.db import models


class OSCARReturnAbstract(models.Model):
    """Used for downloading the Oscar return.
    Mapped to a view in the database, because
    the query is too complex"""

    # Does not inherit from BaseModel as it maps to view
    # The view is created by  migration 0038_auto_create_view_forecast_oscar_return.py

    row_number = models.BigIntegerField()
    # The Treasury Level 5 account returned by the query is the result of a coalesce.
    # It is easier to use it as a foreign key in django
    # for getting the account description
    # than doing another join in the query.
    account_l5_code = models.ForeignKey(
        "treasuryCOA.L5Account",
        on_delete=models.PROTECT,
        db_column="account_l5_code",
    )
    sub_segment_code = models.CharField(max_length=8, primary_key=True)
    sub_segment_long_name = models.CharField(max_length=255)
    organization_code = models.CharField(max_length=50)
    organization_alias = models.CharField(max_length=255)
    # Treasury requires the returns in 1000. The query perform the required
    #  division and rounding.
    apr = models.BigIntegerField(default=0)
    may = models.BigIntegerField(default=0)
    jun = models.BigIntegerField(default=0)
    jul = models.BigIntegerField(default=0)
    aug = models.BigIntegerField(default=0)
    sep = models.BigIntegerField(default=0)
    oct = models.BigIntegerField(default=0)
    nov = models.BigIntegerField(default=0)
    dec = models.BigIntegerField(default=0)
    jan = models.BigIntegerField(default=0)
    feb = models.BigIntegerField(default=0)
    mar = models.BigIntegerField(default=0)
    adj1 = models.BigIntegerField(default=0)
    adj2 = models.BigIntegerField(default=0)
    adj3 = models.BigIntegerField(default=0)

    class Meta:
        abstract = True
        db_table = "oscar_return_oscarreturn"
        ordering = ["sub_segment_code"]


class OSCARReturn(OSCARReturnAbstract):
    class Meta:
        managed = False
        db_table = "oscar_return_oscarreturn"
        ordering = ["sub_segment_code"]


class HistoricOSCARReturn(OSCARReturnAbstract):
    financial_year = models.IntegerField()

    class Meta:
        managed = False
        db_table = "oscar_return_historicaloscarreturn"
        ordering = ["sub_segment_code"]
