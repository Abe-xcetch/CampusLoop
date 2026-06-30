from django.contrib import admin

from listings.models import (
    Category,
    Listing,
    ListingApproval,
    ListingApprovalStatus,
    ApprovalDecision,
)
from django.utils import timezone


def approve_listings(modeladmin, request, queryset):
    for listing in queryset:
        if listing.approval_status != ListingApprovalStatus.PENDING:
            continue
        # Update the existing approval record (if present) or create one
        approval, created = ListingApproval.objects.get_or_create(
            listing=listing,
            defaults={
                "reviewed_by": request.user,
                "reviewed_at": timezone.now(),
                "decision": ApprovalDecision.APPROVED,
                "notes": "Bulk approved via admin action",
            },
        )
        if not created:
            approval.reviewed_by = request.user
            approval.reviewed_at = timezone.now()
            approval.decision = ApprovalDecision.APPROVED
            approval.notes = "Bulk approved via admin action"
            approval.save()


def reject_listings(modeladmin, request, queryset):
    for listing in queryset:
        if listing.approval_status != ListingApprovalStatus.PENDING:
            continue
        approval, created = ListingApproval.objects.get_or_create(
            listing=listing,
            defaults={
                "reviewed_by": request.user,
                "reviewed_at": timezone.now(),
                "decision": ApprovalDecision.REJECTED,
                "notes": "Bulk rejected via admin action",
            },
        )
        if not created:
            approval.reviewed_by = request.user
            approval.reviewed_at = timezone.now()
            approval.decision = ApprovalDecision.REJECTED
            approval.notes = "Bulk rejected via admin action"
            approval.save()


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
    actions = [approve_listings, reject_listings]


@admin.register(ListingApproval)
class ListingApprovalAdmin(admin.ModelAdmin):
    list_display = ("listing", "get_seller", "decision", "reviewed_by", "reviewed_at")
    list_filter = ("decision",)
    readonly_fields = ("id", "created_at", "updated_at")
    raw_id_fields = ("listing", "reviewed_by")

    def get_seller(self, obj):
        return obj.listing.seller

    get_seller.short_description = "Seller"
