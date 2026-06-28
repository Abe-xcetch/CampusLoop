from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "role", "is_verified", "is_active", "created_at")
    list_filter = ("role", "is_verified", "is_active", "is_staff")
    search_fields = ("email", "username", "firebase_uid", "first_name", "last_name")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "last_login", "date_joined")

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "CampusLoop Profile",
            {
                "fields": (
                    "id",
                    "firebase_uid",
                    "phone_number",
                    "avatar_url",
                    "role",
                    "is_verified",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "CampusLoop Profile",
            {"fields": ("email", "firebase_uid", "role")},
        ),
    )
