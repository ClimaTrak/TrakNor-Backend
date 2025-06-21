"""Admin configuration for the custom user model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from traknor.infrastructure.accounts.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "first_name", "last_name", "role", "is_staff"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "role", "date_joined")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("date_joined",)
