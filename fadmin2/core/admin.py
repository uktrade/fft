from django.contrib import admin


from .models import AdminInfo, EventLog

class AdminreadOnly(admin.ModelAdmin):
    """Admin class removing create/edit/delete on the model useful for structures created elsewhere and not changeable by DIT, like Treasury """
    # different fields visible if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

    # Remove delete from the list of action
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Don't allow add
    def has_add_permission(self, request):
        return False

    # Don't allow delete
    def has_delete_permission(self, request, obj=None):
        return False

    # unfortunately, I cannot find a way to remove the 'save' button.



class AdminEditOnly(admin.ModelAdmin):
    """Admin class removing edit on the model useful for structures created elsewhere, where DIT wants to add useful tags """
    # different fields visible if updating or creating the object
     # Remove delete from the list of action
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Don't allow add
    def has_add_permission(self, request):
        return False

    # Don't allow delete
    def has_delete_permission(self, request, obj=None):
        return False

    # unfortunately, I cannot find a way to remove the 'save' button.

admin.site.register(AdminInfo)
admin.site.register(EventLog)
