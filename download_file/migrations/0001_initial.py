# Generated by Django 2.2.8 on 2020-01-09 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('document_type', models.CharField(choices=[('Oscar', 'Actuals'), ('Forecast', 'Budget')], default='Forecast', max_length=70)),
                ('status', models.CharField(choices=[('unprocessed', 'Unprocessed'), ('downloaded', 'Downloaded'), ('error', 'Error')], default='unprocessed', max_length=11)),
                ('user_error_message', models.CharField(blank=True, max_length=1000, null=True)),
                ('error_message', models.CharField(blank=True, max_length=255, null=True)),
                ('downloading_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]