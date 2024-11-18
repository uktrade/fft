from django.db import models
from django.core.validators import RegexValidator


class Employee(models.Model):
    cost_centre = models.ForeignKey(
        "costcentre.CostCentre",
        models.PROTECT,
    )
    # I've been informed that an employee should only be associated to a single
    # programme code. However, programme codes are actually assigned on a per pay
    # element basis and in some cases an employee can be associated to multiple. This is
    # seen as an edge case and we want to model it such that an employee only has a
    # single programme code. We will have to handle this discrepancy somewhere.
    programme_code = models.ForeignKey(
        "chartofaccountDIT.ProgrammeCode",
        models.PROTECT,
    )
    employee_no = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f"{self.employee_no} - {self.first_name} {self.last_name}"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


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
    # period 1 -> 12 = apr -> mar
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

    @periods.setter
    def periods(self, value: list[bool]) -> None:
        for i, enabled in enumerate(value):
            setattr(self, f"period_{i + 1}", enabled)


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


class RecruitmentType(models.TextChoices):
    EXPRESSION_OF_INTEREST = "expression_of_interest", "Expression of Interest"
    EXTERNAL_RECRUITMENT_NON_BULK = (
        "external_recruitment_non_bulk",
        "External Recruitment (Non Bulk)",
    )
    EXTERNAL_RECRUITMENT_BULK = (
        "external_recruitment_bulk",
        "External Recruitment (Bulk campaign)",
    )
    INTERNAL_MANAGED_MOVE = "internal_managed_move", "Internal Managed Move"
    INTERNAL_REDEPLOYMENT = "internal_redeployment", "Internal Redeployment"
    OTHER = "other", "Other"
    INACTIVE_POST = "inactive_post", "Inactive Post"
    EXPECTED_UNKNOWN_LEAVERS = "expected_unknown_leavers", "Expected Unknown Leavers"
    MISSING_STAFF = "missing_staff", "Missing Staff"


class RecruitmentStage(models.IntegerChoices):
    PREPARING = 1, "Preparing"
    ADVERT = 2, "Advert (Vac ref to be provided)"
    SIFT = 3, "Sift"
    INTERVIEW = 4, "Interview"
    ONBOARDING = 5, "Onboarding"
    UNSUCCESSFUL_RECRUITMENT = 6, "Unsuccessful recruitment"
    NOT_YET_ADVERTISED = 7, "Not (yet) advertised"
    NOT_REQUIRED = 8, "Not required"


class Vacancy(models.Model):
    class Meta:
        verbose_name_plural = "Vacancies"

    cost_centre = models.ForeignKey("costcentre.CostCentre", models.PROTECT)

    grade = models.ForeignKey("gifthospitality.Grade", models.PROTECT)
    programme_code = models.ForeignKey("chartofaccountDIT.ProgrammeCode", models.PROTECT)
    recruitment_type = models.CharField(
        max_length=29,
        choices=RecruitmentType.choices,
        default=RecruitmentType.EXPRESSION_OF_INTEREST,
    )
    recruitment_stage = models.IntegerField(
        choices=RecruitmentStage.choices, default=RecruitmentStage.PREPARING
    )

    appointee_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z '-]*$",
                message="Only letters, spaces, - and ' are allowed",
            )
        ],
    )
    hiring_manager = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z '-]*$",
                message="Only letters, spaces, - and ' are allowed",
            )
        ],
    )
    hr_ref = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z '-]*$",
                message="Only letters, spaces, - and ' are allowed",
            )
        ],
    )
