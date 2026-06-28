from django.contrib import admin

from transactions.models import Review, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "buyer", "seller", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("listing__title", "buyer__email", "seller__email")
    readonly_fields = ("id", "created_at", "updated_at")
    raw_id_fields = ("listing", "buyer", "seller")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("transaction", "reviewer", "reviewee", "rating", "created_at")
    list_filter = ("rating",)
    readonly_fields = ("id", "created_at", "updated_at")
    raw_id_fields = ("transaction", "reviewer", "reviewee")
