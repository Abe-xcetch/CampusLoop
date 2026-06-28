from django.contrib import admin

from reports.models import FraudReport


@admin.register(FraudReport)
class FraudReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reporter",
        "reason",
        "status",
        "reported_user",
        "reported_listing",
        "reported_transaction",
        "created_at",
    )
    list_filter = ("status", "reason")
    search_fields = ("reporter__email", "details")
    readonly_fields = ("id", "created_at", "updated_at")
    raw_id_fields = (
        "reporter",
        "reported_user",
        "reported_listing",
        "reported_transaction",
        "resolved_by",
    )
