from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Case, F, Q, Sum, When


class EmployeeQuerySet(models.QuerySet):
    def with_basic_pay(self):
        return self.annotate(
            basic_pay=Sum(
                F("pay_element__debit_amount") - F("pay_element__credit_amount"),
                # TODO (FFT-107): Resolve hard-coded references to "Basic Pay"
                # This might change when we get round to ingesting the data, so I'm OK
                # with it staying like this for now.
                filter=Q(pay_element__type__group__name="Basic Pay"),
                default=0,
                output_field=models.FloatField(),
            )
        )

    def payroll(self):
        return self.filter(basic_pay__gt=0)


class Position(models.Model):
    class Meta:
        abstract = True

    cost_centre = models.ForeignKey(
        "costcentre.CostCentre",
        models.PROTECT,
    )
    programme_code = models.ForeignKey(
        "chartofaccountDIT.ProgrammeCode",
        models.PROTECT,
    )
    grade = models.ForeignKey(to="gifthospitality.Grade", on_delete=models.PROTECT)
    fte = models.FloatField(default=1.0)


class PositionPayPeriods(models.Model):
    class Meta:
        abstract = True

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
    notes = models.TextField(default="")

    @property
    def periods(self) -> list[bool]:
        return [getattr(self, f"period_{i + 1}") for i in range(12)]

    @periods.setter
    def periods(self, value: list[bool]) -> None:
        for i, enabled in enumerate(value):
            setattr(self, f"period_{i + 1}", enabled)


class Employee(Position):
    employee_no = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    assignment_status = models.CharField(max_length=32)
    basic_pay = models.BigIntegerField(default=0, db_comment="pence")
    pension = models.BigIntegerField(default=0, db_comment="pence")
    ernic = models.BigIntegerField(default=0, db_comment="pence")
    has_left = models.BooleanField(default=False)
    is_payroll = models.GeneratedField(
        expression=Case(When(basic_pay__gt=0, then=True), default=False),
        output_field=models.BooleanField(),
        db_persist=True,
    )

    # TODO: Missing fields from Admin Tool which aren't required yet.
    # EU/Non-EU (from programme code model)

    objects = EmployeeQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.employee_no} - {self.first_name} {self.last_name}"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class EmployeePayPeriods(PositionPayPeriods):
    class Meta:
        verbose_name_plural = "employee pay periods"
        constraints = [
            models.UniqueConstraint(
                fields=("employee", "year"),
                name="unique_employee_pay_periods",
            )
        ]

    employee = models.ForeignKey(Employee, models.PROTECT, related_name="pay_periods")

    # TODO: Missing fields from Admin Tool which aren't required yet.
    # capital (Real colour of money)
    # recharge = models.CharField(max_length=50, null=True, blank=True)
    # recharge_reason = models.CharField(max_length=100, null=True, blank=True)


# aka "ToolTypePayment"
class PayElementTypeGroup(models.Model):
    name = models.CharField(max_length=32, unique=True)
    natural_code = models.ForeignKey("chartofaccountDIT.NaturalCode", models.PROTECT)

    def __str__(self) -> str:
        return self.name


class Vacancy(Position):
    class Meta:
        verbose_name_plural = "Vacancies"

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
        EXPECTED_UNKNOWN_LEAVERS = (
            "expected_unknown_leavers",
            "Expected Unknown Leavers",
        )
        MISSING_STAFF = "missing_staff", "Missing Staff"

    recruitment_type = models.CharField(
        max_length=29,
        choices=RecruitmentType.choices,
        default=RecruitmentType.EXPRESSION_OF_INTEREST,
    )

    class RecruitmentStage(models.IntegerChoices):
        PREPARING = 1, "Preparing"
        ADVERT = 2, "Advert - vacancy reference to be provided"
        SIFT = 3, "Sift"
        INTERVIEW = 4, "Interview"
        ONBOARDING = 5, "Onboarding"
        UNSUCCESSFUL_RECRUITMENT = 6, "Unsuccessful recruitment"
        NOT_YET_ADVERTISED = 7, "Not yet advertised"
        NOT_REQUIRED = 8, "Not required"

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
                message="Only letters, spaces, - and ' are allowed.",
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
                message="Only letters, spaces, - and ' are allowed.",
            )
        ],
    )
    hr_ref = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9 '-]*$",
                message="Only letters, numbers, spaces, - and ' are allowed.",
            )
        ],
    )


class VacancyPayPeriods(PositionPayPeriods):
    class Meta:
        verbose_name_plural = "vacancy pay periods"
        constraints = [
            models.UniqueConstraint(
                fields=("vacancy", "year"),
                name="unique_vacancy_pay_periods",
            )
        ]

    vacancy = models.ForeignKey(Vacancy, models.CASCADE, related_name="pay_periods")
