from django.contrib import admin

from reputation.models import ReputationScore


@admin.register(ReputationScore)
class ReputationScoreAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "rating_average",
        "total_ratings_count",
        "completed_transactions_count",
        "is_trusted_seller",
        "updated_at",
    )
    list_filter = ("is_trusted_seller",)
    search_fields = ("user__email",)
    readonly_fields = ("id", "created_at", "updated_at")
    raw_id_fields = ("user",)
