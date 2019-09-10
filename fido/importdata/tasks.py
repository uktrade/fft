from celery import shared_task

from datetime import datetime

from .models import AsyncImportLog

@shared_task
def import_task(requester, type, file, import_func):
    print('Started')
    log = AsyncImportLog(import_type = type, import_status = AsyncImportLog.STATUS_STARTED, imported_by = requester)
    log.save
    return True

    logid = log.id
    result = True
    # result, message = import_func(file)
    message = ''
    if result:
        status = AsyncImportLog.STATUS_COMPLETED
        message = 'Inport successful.'
    else:
        status = AsyncImportLog.STATUS_FAILED

    log = AsyncImportLog(id = logid, import_status = status, import_message = message, import_end=datetime.now())
    log.save
    print('Completed')
    return result