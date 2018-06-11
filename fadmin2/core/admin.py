from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import AdminInfo, EventLog

from django.utils.encoding import smart_str
import openpyxl
from openpyxl.utils import get_column_letter

# http://blog.aeguana.com/2015/12/12/csv-export-data-for-django-model/
from django.db import models
from django.http import StreamingHttpResponse


admin.site.register(AdminInfo)
admin.site.register(EventLog)
