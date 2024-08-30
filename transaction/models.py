from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)
    cost_centre = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    line_description = models.TextField()
    net = models.DecimalField(max_digits=10, decimal_places=2)
    fiscal_period = models.CharField(max_length=100)
    date_of_journal = models.DateField()
    purchase_order_number = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100)
    level4_code = models.CharField(max_length=100)

    def __str__(self):
        return self.transaction_id