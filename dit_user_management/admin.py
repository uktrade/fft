from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

# from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    fieldsets = (
        (_('Login Info'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Account Status'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Groups and User Permissions'), {'fields': ('groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ['last_login', 'date_joined', 'password']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Disable functionality to add user from admin interface
    # This is to ensure, user is entered strictly via SSO auth
    def has_add_permission(self, request):
        return False
