from django.core.management.base import BaseCommand

import core

from gifthospitality.models import (
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
    Grade,
)


class GiftAndHospitalityCategories:
    name = "Gift and Hospitality Categories"

    def clear(self):
        GiftAndHospitalityCategory.objects.all().delete()

    def create(self):
        self.clear()
        GiftAndHospitalityCategory.objects.create(
            gif_hospitality_category='Meeting company to discuss Trade and/or Investment opportunities', # noqa
            active=True,
            sequence_no=10,
        )
        GiftAndHospitalityCategory.objects.create(
            gif_hospitality_category='Attended company event (reception/conference) whom we assisted', # noqa
            active=True,
            sequence_no=20,
        )
        GiftAndHospitalityCategory.objects.create(
            gif_hospitality_category='Attended event for networking purpose (getting to know companies/industry)', # noqa
            active=True,
            sequence_no=30,
        )
        GiftAndHospitalityCategory.objects.create(
            gif_hospitality_category='Attended to give a speech',
            active=True,
            sequence_no=40,
        )
        GiftAndHospitalityCategory.objects.create(
            gif_hospitality_category='Other',
            active=True,
            sequence_no=2000,
        )


class GiftAndHospitalityCompanies:
    name = "Gift and Hospitality Companies"

    def clear(self):
        GiftAndHospitalityCompany.objects.all().delete()

    def create(self):
        self.clear()
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='ADS',
            active=True,
            sequence_no=10,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='Augusta Westland',
            active=True,
            sequence_no=30,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='BAES',
            active=True,
            sequence_no=40,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='Ernst & Young',
            active=True,
            sequence_no=90,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='Lockheed Martin',
            active=True,
            sequence_no=120,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='MBDA',
            active=True,
            sequence_no=130,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='PWC',
            active=True,
            sequence_no=150,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='Rolls Royce',
            active=True,
            sequence_no=170,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='Selex Galileo',
            active=True,
            sequence_no=180,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='Thales UK',
            active=True,
            sequence_no=190,
        )
        GiftAndHospitalityCompany.objects.create(
            gif_hospitality_company='Other',
            active=True,
            sequence_no=100000,
        )


class GiftAndHospitalityClassifications:
    name = "Gift and Hospitality Types"

    def clear(self):
        GiftAndHospitalityClassification.objects.all().delete()

    def create(self):
        self.clear()
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Breakfast',
            active=True,
            sequence_no=10,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Lunch',
            active=True,
            sequence_no=20,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Dinner (Private)',
            active=True,
            sequence_no=30,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Dinner (Public)',
            active=True,
            sequence_no=40,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Reception',
            active=True,
            sequence_no=50,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Gift',
            gif_hospitality_classification='Gifts',
            active=True,
            sequence_no=60,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Sporting/Cultural Event',
            active=True,
            sequence_no=70,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Hotel',
            active=True,
            sequence_no=80,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Transport',
            active=True,
            sequence_no=90,
        )
        GiftAndHospitalityClassification.objects.create(
            gift_type='Hospitality',
            gif_hospitality_classification='Drinks',
            active=True,
            sequence_no=100,
        )


class Grades:
    name = "Grades"

    def clear(self):
        Grade.objects.all().delete()

    def create(self):
        self.clear()
        Grade.objects.create(
            grade='Contractor',
            gradedescription='Unknown',
            active=True,
        )
        Grade.objects.create(
            grade='SEO',
            gradedescription='SEO',
            active=True,
        )
        Grade.objects.create(
            grade='SCS',
            gradedescription='Senior Civil Service 1 and 2',
            active=True,
        )
        Grade.objects.create(
            grade='HEO',
            gradedescription='HEO',
            active=True,
        )
        Grade.objects.create(
            grade='Grade 7',
            gradedescription='Grade 7',
            active=True,
        )
        Grade.objects.create(
            grade='Grade 6',
            gradedescription='Grade 6',
            active=True,
        )
        Grade.objects.create(
            grade='Faststream',
            gradedescription='Faststream',
            active=True,
        )
        Grade.objects.create(
            grade='EO',
            gradedescription='EO',
            active=True,
        )
        Grade.objects.create(
            grade='AO',
            gradedescription='AO',
            active=True,
        )
        Grade.objects.create(
            grade='AA',
            gradedescription='AA',
            active=True,
        )


class Command(BaseCommand):
    GIFT_HOSPITALITY_TABLES = {
        "GiftAndHospitalityCategories": GiftAndHospitalityCategories,
        "GiftAndHospitalityCompanies": GiftAndHospitalityCompanies,
        "GiftAndHospitalityClassifications": GiftAndHospitalityClassifications,
        "Grades": Grades,
    }

    help = "Create Gift and Hospitality data. Allowed types are - All - {}".format(
        " - ".join(GIFT_HOSPITALITY_TABLES.keys())
    )
    arg_name = "what"

    def add_arguments(self, parser):
        # Positional arguments, default to All for no argument
        parser.add_argument(self.arg_name, nargs="*", default=["All"])

        # Named (optional) arguments
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete Gift and Hospitality data instead of creating it",
        )

    def create(self, what):
        core._called_from_test = True
        p = what()
        p.create()
        del core._called_from_test
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully completed G and H data creation for {}.".format(
                    p.name
                )
            )
        )

    def clear(self, what):
        core._called_from_test = True
        p = what()
        p.clear()
        del core._called_from_test
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully cleared Gift and Hospitality data for {}.".format(
                    p.name
                )
            )
        )

    def handle(self, *args, **options):
        if options["delete"]:
            func = self.clear
        else:
            func = self.create
        for arg in options[self.arg_name]:
            if arg == "All":
                for t in self.GIFT_HOSPITALITY_TABLES.values():
                    func(t)
                return
            else:
                func(self.GIFT_HOSPITALITY_TABLES[arg])
