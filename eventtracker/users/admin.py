from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUsers


class CustomUsersAdmin(UserAdmin):
    prepopulated_fields = {"slug": ("first_name", "last_name",)}
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'slug'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'slug')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )


admin.site.register(CustomUsers, CustomUsersAdmin)
