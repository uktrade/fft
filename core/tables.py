import django_tables2 as tables





class FadminTable(tables.Table):
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table-bordered small-font"}
        empty_text = "There are no data matching the search criteria..."



