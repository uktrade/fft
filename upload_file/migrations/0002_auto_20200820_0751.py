# Generated by Django 2.2.13 on 2020-08-20 07:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("upload_file", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fileupload",
            name="document_file",
        ),
        migrations.RemoveField(
            model_name="simplehistoryfileupload",
            name="document_file",
        ),
        migrations.AddField(
            model_name="fileupload",
            name="document_file_name",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="fileupload",
            name="file_location",
            field=models.CharField(
                choices=[
                    ("actuals", "Actuals"),
                    ("budget", "Budget"),
                    ("previousyear", "Previous Year"),
                ],
                default="S3",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="fileupload",
            name="s3_document_file",
            field=models.FileField(
                blank=True, max_length=1000, null=True, upload_to=""
            ),
        ),
        migrations.AddField(
            model_name="simplehistoryfileupload",
            name="document_file_name",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="simplehistoryfileupload",
            name="file_location",
            field=models.CharField(
                choices=[
                    ("actuals", "Actuals"),
                    ("budget", "Budget"),
                    ("previousyear", "Previous Year"),
                ],
                default="S3",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="simplehistoryfileupload",
            name="s3_document_file",
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="fileupload",
            name="document_type",
            field=models.CharField(
                choices=[
                    ("actuals", "Actuals"),
                    ("budget", "Budget"),
                    ("previousyear", "Previous Year"),
                ],
                default="actuals",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="fileupload",
            name="uploading_user",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="simplehistoryfileupload",
            name="document_type",
            field=models.CharField(
                choices=[
                    ("actuals", "Actuals"),
                    ("budget", "Budget"),
                    ("previousyear", "Previous Year"),
                ],
                default="actuals",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="simplehistoryfileupload",
            name="uploading_user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
