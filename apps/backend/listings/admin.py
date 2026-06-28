from django.contrib import admin

from listings.models import Category, Listing, ListingApproval


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "category", "price", "approval_status", "created_at")
    list_filter = ("approval_status", "condition", "category")
    search_fields = ("title", "description", "seller__email")
    readonly_fields = ("id", "created_at", "updated_at")
    raw_id_fields = ("seller", "category")


@admin.register(ListingApproval)
class ListingApprovalAdmin(admin.ModelAdmin):
    list_display = ("listing", "decision", "reviewed_by", "created_at")
    list_filter = ("decision",)
    readonly_fields = ("id", "created_at", "updated_at")
    raw_id_fields = ("listing", "reviewed_by")
