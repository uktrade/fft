# Generated by Django 4.2.15 on 2024-10-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("upload_file", "0005_auto_20230428_1106"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="simplehistoryfileupload",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical file upload",
                "verbose_name_plural": "historical file uploads",
            },
        ),
        migrations.AlterField(
            model_name="simplehistoryfileupload",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]
