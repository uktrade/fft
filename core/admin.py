import io

from django import forms
from django.contrib import admin, messages
from django.contrib.admin.models import (
    CHANGE,
    DELETION,
    LogEntry,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import escape

from core.exportutils import (
    export_csv_from_import,
    export_to_excel,
)
from core.exportutils import export_to_csv
from core.models import FinancialYear


class LogEntryAdmin(admin.ModelAdmin):
    """ Display the Admin log in the Admin interface"""

    date_hierarchy = "action_time"

    # make everything readonly
    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [
                field.name for field in obj.__class__._meta.fields
            ]
        return self.readonly_fields

    list_filter = ["user", "content_type", "action_flag"]

    search_fields = ["object_repr", "change_message"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_flag_",
        "change_message",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != "POST"

    def has_delete_permission(self, request, obj=None):
        return False

    def action_flag_(self, obj):
        flags = {1: "Addition", 2: "Changed", 3: "Deleted"}
        return flags[obj.action_flag]

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse(
                    "admin:%s_%s_change" % (ct.app_label, ct.model),
                    args=[obj.object_id],
                ),
                escape(obj.object_repr),
            )
        return link

    object_link.allow_tags = True
    object_link.admin_order_field = "object_repr"
    object_link.short_description = u"object"


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(FinancialYear)


class AdminActiveField(admin.ModelAdmin):
    """Admin class including the
    handling for the active flag """

    def change_active_flag(self, request, queryset, new_active_value):
        if new_active_value is True:
            msg = "activated"
        else:
            msg = "deactivated"
        q = queryset.filter(active=not new_active_value)
        ct = ContentType.objects.get_for_model(
            queryset.model
        )  # for_model --> get_for_model
        for obj in q:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=CHANGE,
                change_message=str(obj) + " " + msg,
            )
        rows_updated = q.update(active=new_active_value)
        if rows_updated == 1:
            message_bit = "1 {} was".format(queryset.model._meta.verbose_name)
        else:
            message_bit = "{} {} were ".format(
                rows_updated, queryset.model._meta.verbose_name_plural
            )
        self.message_user(request, "{} successfully {}.".format(message_bit, msg))

    def make_inactive(self, request, queryset):
        self.change_active_flag(request, queryset, False)

    def make_active(self, request, queryset):
        self.change_active_flag(request, queryset, True)

    make_inactive.short_description = u"Deactivate the selected object(s)"
    make_active.short_description = u"Activate the selected object(s)"
    actions = [make_inactive, make_active]
    list_filter = ("active",)


class AdminEditOnly(admin.ModelAdmin):
    """Admin class removing edit on
    the model useful for structures
    created elsewhere, where DIT
    wants to add useful tags """

    # Remove delete from the list of action
    def get_actions(self, request):
        actions = super().get_actions(request)

        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    # Don't allow add
    def has_add_permission(self, request):
        return False

    # Don't allow delete
    def has_delete_permission(self, request, obj=None):
        return False


class AdminReadOnly(AdminEditOnly):
    """Admin class removing create/edit/delete
    on the model useful for structures
    created elsewhere and not changeable
    by DIT, like the Treasury """

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [
                field.name for field in obj.__class__._meta.fields
            ]
        return self.readonly_fields


class AdminExport(admin.ModelAdmin):
    change_list_template = "admin/export_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("export-xls/", self.export_all_xls)]
        return my_urls + urls

    def export_all_xls(self, request):
        try:
            queryset = self.queryset_all
        except AttributeError:
            queryset = self.model.objects.all()
            # self.message_user(request, "Export called")
        return export_to_excel(queryset, self.export_func)

    def export_selection_xlsx(self, _, request, queryset):
        # _ is required because the
        # function get called with
        # self passed in twice.
        # Something to do with adding
        # the action in 'get_actions'
        return export_to_excel(queryset, self.export_func)

    # Add export to the list of actions
    def get_actions(self, request):
        # Do it like this to avoid deleting
        # actions defined by other admin
        # model (inheritance)
        actions = super().get_actions(request)
        if "export_selection_xlsx" not in actions:
            actions["export_selection_xlsx"] = (
                self.export_selection_xlsx,
                "export_selection_xlsx",
                u"Export selected object(s) to Excel",
            )
        return actions


class CsvImportForm(forms.Form):
    """Form used to get the file
     to upload for importing data"""

    def __init__(self, header_list, form_title, *args, **kwargs):
        # Form title and header list are
        # used in the template to show
        # the expected fields and the
        # form title.
        self.header_list = header_list
        self.form_title = form_title
        super(CsvImportForm, self).__init__(*args, **kwargs)

    csv_file = forms.FileField()


class AdminImportExport(AdminExport):
    """Used to create an import
    button on the page. Import_dict
    is a property describing the
    import file"""

    change_list_template = "admin/import_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
            path("export-csv/", self.export_csv),
        ]
        return my_urls + urls

    def export_csv(self, request):
        e = export_csv_from_import(self.import_info.key)
        return export_to_csv(e.queryset, e.yield_data)

    def import_csv(self, request):
        header_list = self.import_info.header_list
        import_func = self.import_info.import_func
        form_title = self.import_info.form_title
        check_headers = self.import_info.my_check_headers
        if request.method == "POST":
            form = CsvImportForm(
                header_list,
                form_title,
                request.POST,
                request.FILES,
            )
            if form.is_valid():
                import_file = request.FILES["csv_file"]
                # read() gives you the file
                # contents as a bytes object,
                # on which you can call decode().
                # decode('cp1252') turns your
                # bytes into a string, with known
                # encoding. cp1252 is used to
                # handle single quotes in the strings
                t = io.StringIO(import_file.read().decode("cp1252"))
                success, message = check_headers(t)
                if success:
                    t.seek(0)
                    success, message = import_func(t)
                    if success:
                        return redirect("..")

                messages.error(request, "Error: " + message)
        else:
            form = CsvImportForm(header_list, form_title)
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)


class AdminAsyncImportExport(AdminImportExport):
    def import_csv(self, request):
        header_list = self.import_info.header_list
        import_func = self.import_info.import_func
        form_title = self.import_info.form_title + " ASYNC"
        check_headers = self.import_info.my_check_headers
        if request.method == "POST":
            form = CsvImportForm(
                header_list,
                form_title,
                request.POST,
                request.FILES,
            )
            if form.is_valid():
                import_file = request.FILES["csv_file"]
                # read() gives you the file
                # contents as a bytes object,
                # on which you can call decode().
                # decode('cp1252') turns your
                # bytes into a string, with
                # known encoding. cp1252 is used
                # to handle single quotes in the strings
                t = io.StringIO(import_file.read().decode("cp1252"))
                success, message = check_headers(t)
                if success:
                    t.seek(0)
                    success, message = import_func(t)
                    if success:
                        return redirect("..")

                messages.error(request, "Error: " + message)
        else:
            form = CsvImportForm(
                header_list,
                form_title,
            )

        payload = {
            "form": form
        }

        return render(request, "admin/csv_form.html", payload)


User = get_user_model()


class UserListFilter(admin.SimpleListFilter):
    title = 'users'
    parameter_name = 'users'
    default_value = None

    def lookups(self, request, model_admin):
        list_of_users = []
        users = User.objects.all()

        for user in self.queryset(
            request,
            users,
        ):
            list_of_users.append(
                (str(user.id), user.email)
            )

        return sorted(list_of_users, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if request.user.groups.filter(
            name="Finance Administrator"
        ).exists():
            # Remove super users and fellow finance admins
            super_users = User.objects.filter(is_superuser=True)
            id_list = [user.id for user in super_users]

            # Remove administering user
            id_list.append(request.user.id)

            return queryset.exclude(
                pk__in=id_list
            ).order_by("-email")

        return queryset


class UserAdmin(admin.ModelAdmin):
    list_filter = (UserListFilter,)

    def save_model(self, request, obj, form, change):
        for group in form.cleaned_data["groups"]:
            if group.name in [
                "Finance Business Partner/BSCE",
                "Finance Administrator",
            ]:
                obj.is_staff = True
                break
        else:
            if not obj.is_superuser:
                obj.is_staff = False

        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return None

        return [
            "first_name",
            "password",
            "last_name",
            "email",
            "password",
            "last_login",
            "is_superuser",
            "user_permissions",
            "is_active",
            "is_staff",
            "date_joined",
        ]


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, UserAdmin)
