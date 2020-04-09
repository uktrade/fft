from django.db import DatabaseError

from core.models import FinancialYear


class CheckDatabase:
    name = "database"

    def check(self):
        try:
            FinancialYear.objects.all().exists()
            return True, ""
        except DatabaseError as e:
            return False, e


services_to_check = (CheckDatabase,)
