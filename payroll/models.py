from django.db import models


class Employee(models.Model):
    cost_centre = models.ForeignKey("costcentre.CostCentre", models.PROTECT)
    employee_no = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f"{self.employee_no} - {self.first_name} {self.last_name}"


class EmployeePayPeriods(models.Model):
    class Meta:
        verbose_name_plural = "employee pay periods"
        constraints = [
            models.UniqueConstraint(
                fields=("employee", "year"),
                name="unique_employee_pay_periods",
            )
        ]

    employee = models.ForeignKey(Employee, models.PROTECT, related_name="pay_periods")
    year = models.ForeignKey("core.FinancialYear", models.PROTECT)
    # period 1 = apr, period 2 = may, etc...
    # pariod 1 -> 12 = apr -> mar
    # Here is a useful text snippet:
    #   apr period_1
    #   may period_2
    #   jun period_3
    #   jul period_4
    #   aug period_5
    #   sep period_6
    #   oct period_7
    #   nov period_8
    #   dec period_9
    #   jan period_10
    #   feb period_11
    #   mar period_12
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
class PayElementTypeGroup(models.Model):
    name = models.CharField(max_length=32, unique=True)
    natural_code = models.ForeignKey("chartofaccountDIT.NaturalCode", models.PROTECT)

    def __str__(self) -> str:
        return self.name


class PayElementType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    # aka "account code"
    natural_code = models.ForeignKey("chartofaccountDIT.NaturalCode", models.PROTECT)
    group = models.ForeignKey(PayElementTypeGroup, models.PROTECT)

    def __str__(self) -> str:
        return self.name


class EmployeePayElement(models.Model):
    """A many-to-many through model that represents an employee's pay make-up."""

    employee = models.ForeignKey(Employee, models.PROTECT, related_name="pay_element")
    type = models.ForeignKey(PayElementType, models.PROTECT)
    # Support up to 9,999,999.99.
    debit_amount = models.DecimalField(max_digits=9, decimal_places=2)
    # Support up to 9,999,999.99.
    credit_amount = models.DecimalField(max_digits=9, decimal_places=2)
