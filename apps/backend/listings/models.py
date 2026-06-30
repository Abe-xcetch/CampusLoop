from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from users.models import UUIDTimestampedModel


class Category(UUIDTimestampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ListingApprovalStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    SOLD = "sold", "Sold"


class ListingCondition(models.TextChoices):
    NEW = "new", "New"
    LIKE_NEW = "like_new", "Like New"
    GOOD = "good", "Good"
    FAIR = "fair", "Fair"


class Listing(UUIDTimestampedModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=15, choices=ListingCondition.choices)
    approval_status = models.CharField(
        max_length=20,
        choices=ListingApprovalStatus.choices,
        default=ListingApprovalStatus.PENDING,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="listings",
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )

    class Meta:
        db_table = "listings"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["approval_status"]),
            models.Index(fields=["seller", "approval_status"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.approval_status})"


class ApprovalDecision(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class ListingApproval(UUIDTimestampedModel):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="approvals",
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listing_approvals",
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "listing_approvals"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.listing.title} - {self.decision}"

    def clean(self):
        super().clean()
        # Only enforce that APPROVED/REJECTED decisions are applied to listings
        # that are currently pending. Allow creating/updating PENDING approval
        # records even if the listing status is different to avoid blocking
        # automatic initialization or administrative corrections.
        if (
            self.listing_id
            and self.decision in (ApprovalDecision.APPROVED, ApprovalDecision.REJECTED)
            and self.listing.approval_status != ListingApprovalStatus.PENDING
        ):
            raise ValidationError(
                "Listing approval can only be recorded for pending listings."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        # If approving and no reviewed_at provided, set it before saving to avoid extra DB updates
        if self.decision == ApprovalDecision.APPROVED and not self.reviewed_at:
            from django.utils import timezone

            self.reviewed_at = timezone.now()

        super().save(*args, **kwargs)

        # Only update listing status for explicit approve/reject actions
        if self.decision == ApprovalDecision.APPROVED:
            self.listing.approval_status = ListingApprovalStatus.APPROVED
        elif self.decision == ApprovalDecision.REJECTED:
            self.listing.approval_status = ListingApprovalStatus.REJECTED
        else:
            # leave listing as pending
            return
        self.listing.save(update_fields=["approval_status", "updated_at"])


# Ensure a ListingApproval is created when a Listing is created
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone


@receiver(post_save, sender=Listing)
def create_listing_approval(sender, instance, created, **kwargs):
    if not created:
        return
    # Create a single pending approval record if none exists. Use
    # get_or_create to avoid race conditions and duplicates.
    ListingApproval.objects.get_or_create(
        listing=instance,
        defaults={
            "reviewed_by": None,
            "decision": ApprovalDecision.PENDING,
            "notes": "",
            "reviewed_at": None,
        },
    )
