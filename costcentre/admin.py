from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from guardian.admin import GuardedModelAdminMixin
from guardian.shortcuts import (
    get_users_with_perms,
    remove_perm,
)

from core.admin import (
    AdminActiveField,
    AdminArchived,
    AdminExport,
    AdminImportExport,
    AdminImportExtraExport,
)

from costcentre.exportcsv import (
    export_bp_iterator,
    export_bsce_iterator,
    export_cc_iterator,
    export_directorate_iterator,
    export_group_iterator,
    export_historic_costcentre_iterator,
    export_person_iterator,
)
from costcentre.forms import (
    GivePermissionAdminForm,
    RemovePermissionAdminForm,
)
from costcentre.import_csv import (
    import_cc_class,
    import_cc_dit_specific_class,
    import_departmental_group_class,
    import_director_class,
)
from costcentre.models import (
    BSCEEmail,
    BusinessPartner,
    CostCentre,
    CostCentrePerson,
    DepartmentalGroup,
    Directorate,
    ArchivedCostCentre,
)

from forecast.permission_shortcuts import assign_perm


# Displays extra fields in the list of cost centres
class CostCentreAdmin(GuardedModelAdminMixin, AdminActiveField, AdminImportExtraExport):

    change_form_template = "costcentre/admin/change_form.html"

    list_display = (
        "cost_centre_code",
        "cost_centre_name",
        "directorate_code",
        "directorate_name",
        "group_code",
        "group_name",
        "deputy_director",
        "business_partner",
        "treasury_segment",
        "active",
    )

    def directorate_name(self, instance):
        return instance.directorate.directorate_name

    def directorate_code(self, instance):
        return instance.directorate.directorate_code

    def group_name(self, instance):
        return instance.directorate.group.group_name

    def group_code(self, instance):
        return instance.directorate.group.group_code

    def treasury_segment(self, instance):
        return instance.directorate.group.treasury_segment_fk

    directorate_name.admin_order_field = "directorate__directorate_name"
    directorate_code.admin_order_field = "directorate__directorate_code"
    group_name.admin_order_field = "directorate__group__group_name"
    group_code.admin_order_field = "directorate__group__group_code"
    treasury_segment.admin_order_field = "directorate__group__treasury_segment_fk"

    def get_actions(self, request):
        actions = super().get_actions(request)

        remove_actions = [
            "make_active",
            "make_inactive",
        ]

        if not request.user.is_superuser:
            for action in remove_actions:
                if action in actions:
                    del actions[action]

        return actions

    # limit the entries for specific foreign fields
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "business_partner":
            kwargs["queryset"] = BusinessPartner.objects.filter(active=True)
        if db_field.name == "deputy_director":
            kwargs["queryset"] = CostCentrePerson.objects.filter(active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name="Finance Administrator") or request.user.is_superuser:
            if obj:
                return [
                    "cost_centre_code",
                    "created",
                    "updated",
                ]  # don't allow to edit the code
            else:
                return ["created", "updated"]
        else:
            return self.get_fields(request, obj)

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "cost_centre_code",
                "cost_centre_name",
                "directorate",
                "deputy_director",
                "business_partner",
                "bsce_email",
                "used_for_travel",
                "disabled_with_actual",
                "active",
                "created",
                "updated",
            ]
        else:
            return [
                "cost_centre_code",
                "cost_centre_name",
                "directorate",
                "bsce_email",
                "used_for_travel",
                "deputy_director",
                "business_partner",
                "disabled_with_actual",
                "active",
            ]

    # the export and import function must be defined as
    # properties, to stop getting 'self' as first parameter
    @property
    def export_func(self):
        return export_cc_iterator

    @property
    def import_info(self):
        return import_cc_class

    @property
    def import_extra_info(self):
        return import_cc_dit_specific_class

    search_fields = [
        "cost_centre_code",
        "cost_centre_name",
        "directorate__directorate_code",
        "directorate__directorate_name",
        "directorate__group__group_code",
        "directorate__group__group_name",
        "deputy_director__name",
        "deputy_director__surname",
    ]
    list_filter = (
        "active",
        "disabled_with_actual",
        "used_for_travel",
        ("directorate", RelatedDropdownFilter),
        ("directorate__group", RelatedDropdownFilter),
    )

    autocomplete_fields = ["directorate"]

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path(
                '<cost_centre_id>/change-permission/',
                self.admin_site.admin_view(self.change_permission),
                name='change_permission',
            ),
        ]

        return extra_urls + urls

    def can_change_permissions(self, user, cost_centre):
        # Only super users, finance admins and finance
        # business partners can access this function
        if not user.groups.filter(
            name__in=[
                "Finance Business Partner/BSCE",
                "Finance Administrator",
            ]
        ).exists() and not user.is_superuser:
            return False

        # If the user is an FBP, they should only have permission
        # if they have permission on this cost centre themselves
        if user.has_perm(
            "costcentre.assign_edit_for_own_cost_centres",
        ) and not user.has_perm(
            "change_costcentre",
            cost_centre,
        ):
            return False

        return True

    # flake8: noqa: C901
    def change_permission(self, request, cost_centre_id, *args, **kwargs):
        cost_centre = self.get_object(request, cost_centre_id)
        cost_centre_url = reverse(
            'admin:costcentre_costcentre_change',
            args=[cost_centre_id],
            current_app=self.admin_site.name,
        )

        if not self.can_change_permissions(
            request.user,
            cost_centre,
        ):
            return HttpResponseRedirect(cost_centre_url)

        url = reverse(
            'admin:change_permission',
            args=[cost_centre_id],
            current_app=self.admin_site.name,
        )

        give_permission_form = GivePermissionAdminForm(
            cost_centre=cost_centre,
            user=request.user,
        )
        remove_permission_form = RemovePermissionAdminForm(
            cost_centre=cost_centre,
            user=request.user,
        )

        if request.method == 'POST':
            if 'submit_give_permission' in request.POST:
                give_permission_form = GivePermissionAdminForm(
                    request.POST,
                    cost_centre=cost_centre,
                    user=request.user,
                )

                if give_permission_form.is_valid():
                    user = give_permission_form.cleaned_data["user"]
                    assign_perm(
                        "change_costcentre",
                        user,
                        cost_centre,
                    )
                    self.message_user(
                        request,
                        'Successfully gave user permission '
                        'to edit cost centre forecast',
                    )

                    return HttpResponseRedirect(url)
            elif 'submit_remove_permission' in request.POST:
                remove_permission_form = RemovePermissionAdminForm(
                    request.POST,
                    cost_centre=cost_centre,
                    user=request.user,
                )

                if remove_permission_form.is_valid():
                    if remove_permission_form.cleaned_data["users"].count() == 0:
                        self.message_user(
                            request,
                            'No users selected',
                        )
                    else:
                        for user in remove_permission_form.cleaned_data["users"]:
                            remove_perm("change_costcentre", user, cost_centre)

                        self.message_user(
                            request,
                            'Successfully removed users from cost centre',
                        )

                        return HttpResponseRedirect(url)

        users_with_edit_permission = get_users_with_perms(
            cost_centre,
            attach_perms=True,
        )

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['give_permission_form'] = give_permission_form
        context['users_with_edit_permission'] = users_with_edit_permission
        context['remove_permission_form'] = remove_permission_form
        context['original'] = cost_centre
        context['title'] = "User with permission to edit cost centre"

        return TemplateResponse(
            request,
            "costcentre/admin/change_permission_form.html",
            context,
        )

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True

        cost_centre = self.get_object(request, obj.pk)

        return self.can_change_permissions(
            request.user,
            cost_centre,
        )


class DirectorateAdmin(AdminActiveField, AdminImportExport):
    list_display = (
        "directorate_code",
        "directorate_name",
        "group_code",
        "group_name",
        "director",
        "active",
    )
    search_fields = [
        "directorate_code",
        "directorate_name",
        "group__group_name",
        "group__group_code",
        "director__name",
        "director__surname",
    ]
    list_filter = ("active", ("group", RelatedDropdownFilter))

    def group_name(self, instance):
        return instance.group.group_name

    def group_code(self, instance):
        return instance.group.group_code

    group_name.admin_order_field = "group__group_name"
    group_code.admin_order_field = "group__group_code"

    # limit the list available in the drop downs
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "director":
            kwargs["queryset"] = CostCentrePerson.objects.filter(
                is_director=True, active=True
            )
        if db_field.name == "group":
            kwargs["queryset"] = DepartmentalGroup.objects.filter(active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "directorate_code",
                "created",
                "updated",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "directorate_code",
                "directorate_name",
                "group",
                "director",
                "active",
                "created",
                "updated",
            ]
        else:
            return [
                "directorate_code",
                "directorate_name",
                "group",
                "director",
                "active",
            ]

    @property
    def export_func(self):
        return export_directorate_iterator

    @property
    def import_info(self):
        return import_director_class


class DepartmentalGroupAdmin(AdminActiveField, AdminImportExport):
    list_display = (
        "group_code",
        "group_name",
        "director_general",
        "treasury_segment_fk",
        "active",
    )
    search_fields = [
        "group_code",
        "group_name",
        "director_general__name",
        "director_general__surname",
    ]
    list_filter = ("active", ("treasury_segment_fk", RelatedDropdownFilter))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "director_general":
            kwargs["queryset"] = CostCentrePerson.objects.filter(
                is_dg=True, active=True
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["group_code", "created", "updated"]  # don't allow to edit the code
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "group_code",
                "group_name",
                "director_general",
                "treasury_segment_fk",
                "active",
                "created",
                "updated",
            ]
        else:
            return [
                "group_code",
                "group_name",
                "director_general",
                "treasury_segment_fk",
                "active",
            ]

    @property
    def export_func(self):
        return export_group_iterator

    @property
    def import_info(self):
        return import_departmental_group_class


class BSCEEmailAdmin(AdminActiveField, AdminExport):
    list_display = ("bsce_email", "active")
    search_fields = ["bsce_email"]

    def get_readonly_fields(self, request, obj=None):
        return ["created", "updated"]

    @property
    def export_func(self):
        return export_bsce_iterator


class BusinessPartnerAdmin(AdminActiveField, AdminExport):
    list_display = ("bp_email", "active")
    search_fields = ["name", "surname", "bp_email"]

    def get_readonly_fields(self, request, obj=None):
        return ["created", "updated"]

    @property
    def export_func(self):
        return export_bp_iterator


class CostCentrePersonAdmin(AdminActiveField, AdminExport):
    list_display = ("full_name", "is_dg", "is_director", "active")
    search_fields = ["name", "last_name"]

    list_filter = ("active", "is_director", "is_dg")

    def get_readonly_fields(self, request, obj=None):
        return ["created", "updated"]

    @property
    def export_func(self):
        return export_person_iterator


class HistoricCostCentreAdmin(AdminArchived, AdminExport):
    list_display = (
        "cost_centre_code",
        "cost_centre_name",
        "directorate_code",
        "directorate_name",
        "group_code",
        "group_name",
        "deputy_director_fullname",
        "business_partner_fullname",
        "active",
    )
    search_fields = [
        "cost_centre_code",
        "cost_centre_name",
        "directorate_code",
        "directorate_name",
        "group_code",
        "group_name",
        "deputy_director_fullname",
    ]
    list_filter = (
        "active",
        "disabled_with_actual",
        ("financial_year", RelatedDropdownFilter),
    )
    fields = (
        "financial_year",
        "cost_centre_code",
        "cost_centre_name",
        "directorate_code",
        "directorate_name",
        "director_fullname",
        "group_code",
        "group_name",
        "dg_fullname",
        "deputy_director_fullname",
        "business_partner_fullname",
        "bsce_email",
        "disabled_with_actual",
        "active",
        "archived",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "cost_centre_code",
                "directorate_code",
                "group_code",
                "archived",
            ]
        else:
            return ["created", "archived", "updated"]

    @property
    def export_func(self):
        return export_historic_costcentre_iterator


admin.site.register(CostCentre, CostCentreAdmin)
admin.site.register(DepartmentalGroup, DepartmentalGroupAdmin)
admin.site.register(Directorate, DirectorateAdmin)
admin.site.register(BSCEEmail, BSCEEmailAdmin)
admin.site.register(BusinessPartner, BusinessPartnerAdmin)
admin.site.register(CostCentrePerson, CostCentrePersonAdmin)
admin.site.register(ArchivedCostCentre, HistoricCostCentreAdmin)
