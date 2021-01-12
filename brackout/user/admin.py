from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'date_joined', ]
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    search_fields = ('email', 'name')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'auth_provider')}),
        (_('Personal Info'),
            {'fields': ('name', 'birth_date', 'gender')}),
        (_('Permissions'),
            {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
