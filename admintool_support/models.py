from django.db import models

from core.metamodels import SimpleTimeStampedModel
# Create your models here.
class DownloadLog(SimpleTimeStampedModel):
    download_type = models.CharField('Download Type', max_length=300)
    downloader = models.CharField('Download by', max_length=300)
