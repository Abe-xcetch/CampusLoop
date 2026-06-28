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
        related_name="listing_approvals",
    )
    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "listing_approvals"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.listing.title} - {self.decision}"

    def clean(self):
        super().clean()
        if (
            self.listing_id
            and self.listing.approval_status != ListingApprovalStatus.PENDING
        ):
            raise ValidationError(
                "Listing approval can only be recorded for pending listings."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        if self.decision == ApprovalDecision.APPROVED:
            self.listing.approval_status = ListingApprovalStatus.APPROVED
        else:
            self.listing.approval_status = ListingApprovalStatus.REJECTED
        self.listing.save(update_fields=["approval_status", "updated_at"])
