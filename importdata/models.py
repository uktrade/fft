from django.db import models

class AsyncImportLog(models.Model):
    """Used to log and follow the asyncronous import of data"""
    IMPORT_ADI = 1
    IMPORT_GL = 2

    IMPORT_CHOICE = (
        (IMPORT_ADI, 'ADI file from Admin Tool'),
        (IMPORT_GL, 'GL Report from Oracle')
    )
    STATUS_STARTED = 1
    STATUS_COMPLETED = 2
    STATUS_FAILED = 3

    STATUS_CHOICE = (
        (STATUS_STARTED, 'Started'),
        (STATUS_COMPLETED, 'Completed successfully'),
        (STATUS_FAILED, 'Failed'),
    )
    import_type = models.CharField(choices=IMPORT_CHOICE, max_length=100)
    import_status = models.CharField(choices=STATUS_CHOICE, max_length=100)
    import_message = models.CharField(max_length=100, blank=True)
    imported_by = models.CharField(max_length=300)
    import_start = models.DateTimeField(auto_now_add=True)
    import_end = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = "Import Log"
        verbose_name_plural = "Import Logs"
        ordering = ['-import_start']
