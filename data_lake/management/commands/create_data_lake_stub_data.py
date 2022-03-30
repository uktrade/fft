from django.core.management.base import BaseCommand

from chartofaccountDIT.models import (
    CommercialCategory,
    FCOMapping,
    InterEntity,
    InterEntityL1,
    NaturalCode,
)


class CommercialCategories:
    name = "Commercial Categories"

    def clear(self):
        CommercialCategory.objects.all().delete()

    def create(self):
        self.clear()
        CommercialCategory.objects.create(
            commercial_category="Commercial Category 1",
            description="Commercial Category 1 description",
            active=True,
        )
        CommercialCategory.objects.create(
            commercial_category="Commercial Category 2",
            description="Commercial Category 2 description",
            active=True,
        )
        CommercialCategory.objects.create(
            commercial_category="Commercial Category 3",
            description="Commercial Category 3 description",
            active=True,
        )


class InterEntities:
    name = "Inter Entities"

    def clear(self):
        InterEntity.objects.all().delete()
        InterEntityL1.objects.all().delete()

    def create(self):
        self.clear()
        inter_entity_l1_obj = InterEntityL1.objects.create(
            active=True,
            l1_value="IE1",
            l1_description="IE1 description",
        )
        InterEntity.objects.create(
            active=True,
            l1_value=inter_entity_l1_obj,
            l2_value="Entity 1",
            l2_description="Entity 1 description",
            cpid="123456",
        )
        InterEntity.objects.create(
            active=True,
            l1_value=inter_entity_l1_obj,
            l2_value="Entity 2",
            l2_description="Entity 2 description",
            cpid="123456",
        )
        InterEntity.objects.create(
            active=True,
            l1_value=inter_entity_l1_obj,
            l2_value="Entity 3",
            l2_description="Entity 3 description",
            cpid="123456",
        )


class FCOMappingCodes:
    name = "FCO Mapping codes"

    def clear(self):
        FCOMapping.objects.all().delete()

    def create(self):
        self.clear()
        nac_obj = NaturalCode.objects.all().first()
        FCOMapping.objects.create(
            active=True,
            fco_code=654321,
            fco_description="654321 description",
            account_L6_code_fk=nac_obj,
        )
        FCOMapping.objects.create(
            active=True,
            fco_code=123456,
            fco_description="123456 description",
            account_L6_code_fk=nac_obj,
        )


def create_all():
    FCOMappingCodes().create()
    InterEntities().create()
    CommercialCategories().create()


def delete_all():
    FCOMappingCodes().clear()
    InterEntities().clear()
    CommercialCategories().clear()


class Command(BaseCommand):
    help = "Create extra stub data for exporting to data workspace"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete stub data instead of creating it",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            delete_all()
            action = "deleted"
        else:
            create_all()
            action = "created"

        self.stdout.write(
            self.style.SUCCESS(f"Successfully {action} data lake stub data.")
        )
