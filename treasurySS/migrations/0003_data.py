# Generated by Django 3.2.4 on 2021-07-29 08:49

from django.db import migrations


def create_organizations(apps, schema_editor):
    OrganizationCode = apps.get_model("treasurySS", "OrganizationCode")
    Segment = apps.get_model("treasurySS", "Segment")
    organization_obj = OrganizationCode.objects.create(
        organization_code="UKT013",
        organization_alias="UK TRADE & INVESTMENT",
        active=True,
    )
    Segment.objects.all().update(organization=organization_obj)
    organization_obj = OrganizationCode.objects.create(
        organization_code="TRA013",
        organization_alias="TRADE REMEDIES AUTHORITY (TRA)",
        active=True,
    )
    Segment.objects.filter(segment_code="S013A007").update(
        organization=organization_obj
    )


class Migration(migrations.Migration):

    dependencies = [
        ("treasurySS", "0002_auto_20210729_0846"),
    ]

    operations = [
        migrations.RunPython(create_organizations),
    ]
