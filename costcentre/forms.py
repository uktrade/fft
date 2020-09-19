from django import forms
from django.contrib.auth import get_user_model
from django.forms import Select

from guardian.shortcuts import (
    get_objects_for_user,
    get_users_with_perms,
)

from costcentre.models import (
    ArchivedCostCentre,
    CostCentre,
)


class CostCentreViewModeForm(forms.Form):
    COST_CENTRE_MODES = [
        ('all', 'All cost centres'),
        ('my', 'My cost centres'),
    ]

    mode = forms.ChoiceField(
        choices=COST_CENTRE_MODES,
        widget=forms.RadioSelect,
    )

    mode.widget.attrs.update(
        {
            'onclick': 'swapCostCentreChoice(this)',
        }
    )


class AllCostCentresForm(forms.Form):
    cost_centre = forms.ModelChoiceField(
        queryset=CostCentre.objects.filter(
            active=True,
        ),
        widget=Select(),
    )
    cost_centre.widget.attrs.update(
        {
            "class": "govuk-select",
        }
    )


class DirectorateCostCentresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        year = kwargs.pop('year')
        cost_centre_code = kwargs.pop('cost_centre_code')
        super(DirectorateCostCentresForm, self).__init__(
            *args,
            **kwargs,
        )

        if year:
            directorate_code = ArchivedCostCentre.objects.get(
                cost_centre_code=cost_centre_code,
                financial_year_id=year,
            ).directorate_code
            cost_centre_queryset = ArchivedCostCentre.objects.filter(
                directorate_code=directorate_code,
                financial_year_id=year,
                active=True,
            )
            self.fields['cost_centre'] = forms.ModelChoiceField(
                queryset=cost_centre_queryset,
                widget=Select(),
                initial=cost_centre_code,
                to_field_name='cost_centre_code'
            )
        else:
            directorate_code = CostCentre.objects.get(
                cost_centre_code=cost_centre_code)\
                .directorate.directorate_code
            cost_centre_queryset = CostCentre.objects.filter(
                directorate__directorate_code=directorate_code,
                active=True,
            )
            self.fields['cost_centre'] = forms.ModelChoiceField(
                queryset=cost_centre_queryset,
                widget=Select(),
                initial=cost_centre_code
            )

        self.fields["cost_centre"].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )


class MyCostCentresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        accept_global_perms = False

        if user.has_perm("costcentre.edit_forecast_all_cost_centres"):
            accept_global_perms = True

        self.base_fields['cost_centre'].queryset = get_objects_for_user(
            user,
            "costcentre.change_costcentre",
            accept_global_perms=accept_global_perms,
        )

        super(MyCostCentresForm, self).__init__(
            *args,
            **kwargs,
        )

    cost_centre = forms.ModelChoiceField(
        queryset=None,
        widget=Select(),
    )

    cost_centre.widget.attrs.update(
        {
            "class": "govuk-select",
        }
    )


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_short_name()


class GivePermissionAdminForm(forms.Form):
    def __init__(self, *args, **kwargs):
        User = get_user_model()

        cost_centre = kwargs.pop('cost_centre')
        administering_user = kwargs.pop('user')

        # Filter out all users who already have permission
        users = get_users_with_perms(cost_centre, attach_perms=True)
        id_list = [user.id for user in users]

        # Remove super users
        super_users = User.objects.filter(is_superuser=True)
        id_list = id_list + [user.id for user in super_users]

        # Remove finance admins if user is FBP
        if administering_user.groups.filter(
            name__in=[
                "Finance Business Partner/BSCE",
            ]
        ).exists():
            finance_admin_users = User.objects.filter(
                groups__name='Finance Administrator',
            )
            id_list = id_list + [user.id for user in finance_admin_users]

        # Remove administering user
        id_list.append(administering_user.id)

        # Set list of users removing administering user
        self.base_fields['user'].queryset = User.objects.exclude(
            pk__in=id_list
        ).order_by("-first_name")

        super(GivePermissionAdminForm, self).__init__(
            *args,
            **kwargs,
        )

    user = UserModelChoiceField(
        queryset=None,
        widget=Select(),
    )


class RemovePermissionAdminForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=None,
        label="",
    )

    def __init__(self, *args, **kwargs):
        User = get_user_model()
        cost_centre = kwargs.pop('cost_centre')
        administering_user = kwargs.pop('user')

        users_with_permission = get_users_with_perms(cost_centre, attach_perms=True)
        id_list = [user.id for user in users_with_permission]
        id_list.append(administering_user.id)

        super(RemovePermissionAdminForm, self).__init__(*args, **kwargs)

        self.fields['users'].queryset = User.objects.filter(
            pk__in=id_list
        ).exclude(pk=administering_user.id)
