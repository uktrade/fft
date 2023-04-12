from django.db import models

from chartofaccountDIT.models import NaturalCode


class UploadNaturalCode(models.Model):
    natural_account_code = models.IntegerField(primary_key=True, verbose_name="NAC",)
    gross_income = models.CharField(
        max_length=20,
        choices=NaturalCode.GROSS_INCOME_CHOICE,
        blank=True,
        null=True,
    )
    cash_non_cash = models.CharField(
        max_length=20,
        choices=NaturalCode.CASH_NONCASH_CHOICE,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["natural_account_code"]
