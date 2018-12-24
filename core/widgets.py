from dal.widgets import (
    QuerySetSelectMixin,

)

from django import forms

from dal_select2.widgets import Select2WidgetMixin


class Select2BootstrapWidgetMixin(Select2WidgetMixin):
    @property
    def media(self):
        media = super(Select2BootstrapWidgetMixin, self).Media
        return forms.Media(
            js=media.js,
            css={
                'all': (
                'autocomplete_light/vendor/select2/dist/css/select2.css', # The one from dal_select2.widgets.Select2WidgetMixin
                'css/select2-bootstrap.min.css'  # Bootstrap theme itself
                )
            },
        )

    def build_attrs(self, *args, **kwargs):
        attrs = super(Select2BootstrapWidgetMixin, self).build_attrs(*args, **kwargs)
        attrs.setdefault('data-theme',
                         'bootstrap')
        return attrs


class ModelSelect2Bootstrap(QuerySetSelectMixin,
                            Select2BootstrapWidgetMixin,
                            forms.Select):
    """
    Use this instead of ModelSelect2 widget
    """
    autocomplete_function = 'select2'


class ModelSelect2MultipleBootstrap(QuerySetSelectMixin,
                                    Select2BootstrapWidgetMixin,
                                    forms.Select):
    """
    Use this instead of ModelSelect2Multiple widget
    """
    autocomplete_function = 'select2'
