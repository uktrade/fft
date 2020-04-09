from django.contrib.admin.widgets import AutocompleteSelect


class FormAutocompleteSelect(AutocompleteSelect):
    """Use the admin autocomplete class in a form,
    by passing the name of the model to use in
    the auto complete dropdown.
    Unfortunately, it only works for people with Admin access"""

    class admin_site:
        pass

    class rel:
        pass

    def __init__(self, model, **kwargs):
        self.admin_site.name = "admin"
        self.rel.model = model
        super(FormAutocompleteSelect, self).__init__(
            self.rel, self.admin_site, **kwargs
        )
