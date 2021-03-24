import io

from django import forms
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry

from django.core.files.uploadhandler import (
    MemoryFileUploadHandler,
    TemporaryFileUploadHandler,
)
from django.shortcuts import redirect, render
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from core.export_data import export_logentry_iterator
from core.models import (
    CommandLog,
    FinancialYear,
)
from core.utils.export_helpers import (
    export_csv_from_import,
    export_to_csv,
    export_to_excel,
)
from core.utils.generic_helpers import (
    get_current_financial_year,
    log_object_change,
)


class AdminActiveField(admin.ModelAdmin):
    """Admin class including the
    handling for the active flag """

    def change_active_flag(self, request, queryset, new_active_value):
        if new_active_value is True:
            msg = "activated"
        else:
            msg = "deactivated"
        q = queryset.filter(active=not new_active_value)

        for obj in q:
            log_object_change(
                request.user.id, msg, obj=obj,
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

    make_inactive.short_description = "Deactivate the selected object(s)"
    make_active.short_description = "Activate the selected object(s)"
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
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


class AdminExport(admin.ModelAdmin):
    change_list_template = "admin/export_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("export-xls/", self.export_all_xls)]
        return my_urls + urls

    def export_all_xls(self, request):
        log_object_change(
            request.user.id, f"Export all as .xlsx from {self.__class__.__name__}",
        )

        try:
            queryset = self.queryset_all
        except AttributeError:
            queryset = self.model.objects.all()
        return export_to_excel(queryset, self.export_func)

    def export_selection_xlsx(self, _, request, queryset):
        log_object_change(
            request.user.id, "Export selection as .xlsx",
        )

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
                "Export selected object(s) to Excel",
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
        log_object_change(
            request.user.id, "Export CSV",
        )

        e = export_csv_from_import(self.import_info.key)
        return export_to_csv(e.queryset, e.yield_data)

    def process_csv(self, request, import_info):
        log_object_change(
            request.user.id, "Processing CSV",
        )

        import_file = request.FILES["csv_file"]
        # read() gives you the file
        # contents as a bytes object,
        # on which you can call decode().
        # decode('cp1252') turns your
        # bytes into a string, with known
        # encoding. cp1252 is used to
        # handle single quotes in the strings
        t = io.StringIO(import_file.read().decode("cp1252"))
        success, message = import_info.my_check_headers(t)
        if success:
            t.seek(0)
            success, message = import_info.import_func(t)
        if not success:
            messages.error(request, "Error: " + message)
        return success, message

    @csrf_exempt
    def import_csv(self, request):
        return self.generic_import_csv(request, self.import_info)

    def generic_import_csv(self, request, import_info):
        log_object_change(
            request.user.id, f"Import CSV: '{import_info.form_title}'",
        )

        header_list = import_info.header_list
        form_title = import_info.form_title

        # because the files are small, upload them to memory
        # instead of using S3
        request.upload_handlers.insert(0, TemporaryFileUploadHandler(request))
        request.upload_handlers.insert(0, MemoryFileUploadHandler(request))

        if request.method == "POST":
            form = CsvImportForm(header_list, form_title, request.POST, request.FILES,)
            if form.is_valid():
                success, message = self.process_csv(request, import_info)
                if success:
                    return redirect("..")
        else:
            form = CsvImportForm(header_list, form_title)
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)


class AdminImportExtraExport(AdminImportExport):

    change_list_template = "admin/m_import_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import1-extra-csv/", self.import_extra_csv),
        ]
        return my_urls + urls

    @csrf_exempt
    def import_extra_csv(self, request):
        return self.generic_import_csv(request, self.import_extra_info)


class LogEntryAdmin(AdminReadOnly, AdminExport):
    """ Display the Admin log in the Admin interface"""

    date_hierarchy = "action_time"

    # make everything readonly
    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

    @property
    def export_func(self):
        return export_logentry_iterator

    list_filter = ["user", "content_type", "action_flag"]

    search_fields = ["object_repr", "change_message"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "action_flag_",
        "object_id",
        "object_repr",
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


class FinancialYearAdmin(admin.ModelAdmin):

    list_display = (
        "financial_year",
        "financial_year_display",
        "current",
        "archived",
    )

    fields = (
        "financial_year",
        "financial_year_display",
        "current",
        "archived",
        "archived_at",
    )

    def get_readonly_fields(self, request, obj=None):
        read_list = ["created", "updated", "current", "archived", "archived_at"]
        if obj:
            read_list.append("financial_year")
        return read_list


class AdminArchived(admin.ModelAdmin):
    # limit the entries to archived years
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "financial_year":
            current_year = get_current_financial_year()
            kwargs["queryset"] = FinancialYear.objects.filter(
                financial_year__lte=current_year
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CustomLogModelAdmin(AdminReadOnly, AdminExport):
    # make everything readonly
    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in
                                    obj.__class__._meta.fields]
        return self.readonly_fields

    @property
    def export_func(self):
        return export_logentry_iterator

    list_filter = ["command_name", "executed_by", "executed_at"]

    search_fields = ["command_name", "executed_by"]

    list_display = [
        "command_name",
        "executed_at",
        "executed_by",
        "comment",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(FinancialYear, FinancialYearAdmin)
admin.site.register(CommandLog, CustomLogModelAdmin)
