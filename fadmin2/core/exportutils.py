from django.utils.encoding import smart_str

from django.db import models


class SmartExport:
    # return lists with the header name and the objects from a queryset
    # it only follows one level of foreign key, while I would like to follow at lower levels
    def __init__(self, mydata_qs):
        self.data = mydata_qs
        self.model = mydata_qs.model # get the model
        self.model_fields = self.model._meta.fields + self.model._meta.many_to_many
        # Create CSV headers. Use the verbose name
        self.headers = [self.model._meta.get_field(field.name).verbose_name for field in self.model_fields]

    def get_row(self, obj):
        row = []
        for field in self.model_fields:
            if type(field) == models.ForeignKey:
                val = getattr(obj, field.name)
                if val:
                    val = smart_str(val)
            elif type(field) == models.ManyToManyField:
                # val = u', '.join([item.__unicode__() for item in getattr(obj, field.name).all()])
                val = u', '.join([smart_str(item) for item in getattr(obj, field.name).all()])
            elif field.choices:
                val = getattr(obj, 'get_%s_display'%field.name)()
            else:
                val = smart_str(getattr(obj, field.name))
            row.append(val.encode("utf-8"))
        return row

    def stream(self): # Helper function to inject headers
        if self.headers:
            yield self.headers
        for obj in self.data:
            yield self.get_row(obj)

