from django.db import models


class Staff(models.Model):
    cost_centre = models.ForeignKey("costcentre.CostCentre", models.PROTECT)
    employee_no = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f"{self.employee_no} - {self.first_name} {self.last_name}"


class StaffForecast(models.QuerySet):
    pass


class StaffForecast(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("staff", "year"),
                name="unique_staff_forecast",
            )
        ]

    objects = StaffForecast.as_manager()

    staff = models.ForeignKey(Staff, models.PROTECT, related_name="forecast")
    year = models.ForeignKey("core.FinancialYear", models.PROTECT)
    # period 1 = apr, period 2 = may, etc...
    # pariod 1 -> 12 = apr -> mar
    period_1 = models.BooleanField(default=True)
    period_2 = models.BooleanField(default=True)
    period_3 = models.BooleanField(default=True)
    period_4 = models.BooleanField(default=True)
    period_5 = models.BooleanField(default=True)
    period_6 = models.BooleanField(default=True)
    period_7 = models.BooleanField(default=True)
    period_8 = models.BooleanField(default=True)
    period_9 = models.BooleanField(default=True)
    period_10 = models.BooleanField(default=True)
    period_11 = models.BooleanField(default=True)
    period_12 = models.BooleanField(default=True)

    @property
    def periods(self) -> list[bool]:
        return [getattr(self, f"period_{i + 1}") for i in range(12)]


# aka "ToolTypePayment"
class PayElementGroup(models.Model):
    name = models.CharField(max_length=32, unique=True)
    natural_code = models.ForeignKey("chartofaccountDIT.NaturalCode", models.PROTECT)

    def __str__(self) -> str:
        return self.name


class PayElement(models.Model):
    name = models.CharField(max_length=128, unique=True)
    # aka "account code"
    natural_code = models.ForeignKey("chartofaccountDIT.NaturalCode", models.PROTECT)
    group = models.ForeignKey(PayElementGroup, models.PROTECT)

    def __str__(self) -> str:
        return self.name


class Payroll(models.Model):
    staff = models.ForeignKey(Staff, models.PROTECT)
    pay_element = models.ForeignKey(PayElement, models.PROTECT)
    # Support up to 9,999,999.99.
    debit_amount = models.DecimalField(max_digits=9, decimal_places=2)
    # Support up to 9,999,999.99.
    credit_amount = models.DecimalField(max_digits=9, decimal_places=2)
