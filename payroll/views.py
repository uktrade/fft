from dal import autocomplete
from django.db.models import Q

from .models import DITPeople

class DITPeopleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return DITPeople.objects.none()

        qs = DITPeople.objects.all()

        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q) | Q(surname__istartswith=self.q) )
        return qs