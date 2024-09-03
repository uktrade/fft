from django.db import models


class ZeroTransaction(models.Model):
    entity = models.CharField(max_length=100)
    cost_centre = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    analysis_1 = models.CharField(max_length=100)
    spare_1 = models.CharField(max_length=100, blank=True, null=True)
    spare_2 = models.CharField(max_length=100, blank=True, null=True)

    apr = models.FloatField()
    may = models.FloatField()
    jun = models.FloatField()
    jul = models.FloatField()
    aug = models.FloatField()
    sep = models.FloatField()
    oct = models.FloatField()
    nov = models.FloatField()
    dec = models.FloatField()
    jan = models.FloatField()
    feb = models.FloatField()
    mar = models.FloatField()

    adj1 = models.FloatField(blank=True, null=True)
    adj2 = models.FloatField(blank=True, null=True)
    adj3 = models.FloatField(blank=True, null=True)

    total = models.FloatField()

    def parse_csv(self, file_path):
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ZeroTransactionEntry.objects.create(
                    entity=row['entity'],
                    cost_centre=row['cost_centre'],
                    account=row['account'],
                    programme=row['programme'],
                    analysis_1=row['analysis_1'],
                    spare_1=row.get('spare_1', ''),
                    spare_2=row.get('spare_2', ''),
                    apr=row['apr'],
                    may=row['may'],
                    jun=row['jun'],
                    jul=row['jul'],
                    aug=row['aug'],
                    sep=row['sep'],
                    oct=row['oct'],
                    nov=row['nov'],
                    dec=row['dec'],
                    jan=row['jan'],
                    feb=row['feb'],
                    mar=row['mar'],
                    adj1=row.get('adj1', ''),
                    adj2=row.get('adj2', ''),
                    adj3=row.get('adj3', ''),
                    total=row['total'],
                )

    class Meta:
        verbose_name_plural = "Zero Transaction Entries"

    def __str__(self):
        return f"{self.entity} - {self.cost_centre} - {self.account}"

