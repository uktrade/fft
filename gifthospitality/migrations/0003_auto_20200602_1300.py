# Generated by Django 2.2.10 on 2020-06-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gifthospitality", "0002_data_20200522"),
    ]

    operations = [
        migrations.AddField(
            model_name="giftandhospitality",
            name="company_name",
            field=models.CharField(
                blank=True, default="", max_length=200, verbose_name="Other company"
            ),
        ),
        migrations.AddField(
            model_name="simplehistorygiftandhospitality",
            name="company_name",
            field=models.CharField(
                blank=True, default="", max_length=200, verbose_name="Other company"
            ),
        ),
        migrations.RenameField(
            model_name="giftandhospitality",
            old_name="date_offered",
            new_name="date_agreed",
        ),
        migrations.RenameField(
            model_name="simplehistorygiftandhospitality",
            old_name="date_offered",
            new_name="date_agreed",
        ),
        migrations.AlterField(
            model_name="giftandhospitality",
            name="date_agreed",
            field=models.DateField(verbose_name="Date of event /  gift received"),
        ),
        migrations.AlterField(
            model_name="simplehistorygiftandhospitality",
            name="date_agreed",
            field=models.DateField(verbose_name="Date of event /  gift received"),
        ),
    ]
