from django.contrib import admin

from admin_panel.models import AdminAction


@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ("admin", "action_type", "target_id", "created_at")
    list_filter = ("action_type",)
    search_fields = ("admin__email", "notes")
    readonly_fields = ("id", "created_at", "updated_at")
    raw_id_fields = ("admin",)
