from django.db import models


class DownloadLog(models.Model):
    CC_AT = 'CC'
    NAC_H_AT = 'NAC H'
    DOWNLOAD_CHOICE = (
        (CC_AT, 'Cost Centre Hierarchy for Admin Tool'),
        (NAC_H_AT, 'NAC Hierarchy for Admin Tool')
    )
    download_type = models.CharField('Download Type', choices=DOWNLOAD_CHOICE, max_length=300)
    downloader = models.CharField('Download by', max_length=300)
    download_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Download Log"
        verbose_name_plural = "Download Logs"
        ordering = ['-download_time']
