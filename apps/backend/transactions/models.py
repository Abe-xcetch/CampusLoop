from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from listings.models import Listing
from users.models import UUIDTimestampedModel


class TransactionStatus(models.TextChoices):
    INITIATED = "initiated", "Initiated"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    VERIFIED = "verified", "Verified"


class Transaction(UUIDTimestampedModel):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="purchases",
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sales",
    )
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.INITIATED,
    )

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=~Q(buyer=models.F("seller")),
                name="transaction_buyer_not_seller",
            ),
        ]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["buyer", "status"]),
            models.Index(fields=["seller", "status"]),
        ]

    def __str__(self):
        return f"Transaction {self.id} ({self.status})"

    def clean(self):
        super().clean()
        if self.buyer_id and self.seller_id and self.buyer_id == self.seller_id:
            raise ValidationError("Buyer and seller must be different users.")
        if self.listing_id and self.seller_id and self.listing.seller_id != self.seller_id:
            raise ValidationError("Seller must match the listing owner.")


class Review(UUIDTimestampedModel):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_given",
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_received",
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    class Meta:
        db_table = "reviews"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["transaction", "reviewer"],
                name="unique_review_per_transaction_reviewer",
            ),
            models.CheckConstraint(
                check=Q(rating__gte=1) & Q(rating__lte=5),
                name="review_rating_between_1_and_5",
            ),
            models.CheckConstraint(
                check=~Q(reviewer=models.F("reviewee")),
                name="review_reviewer_not_reviewee",
            ),
        ]

    def __str__(self):
        return f"Review {self.id} ({self.rating}/5)"

    def clean(self):
        super().clean()
        if self.transaction_id and self.transaction.status != TransactionStatus.VERIFIED:
            raise ValidationError("Reviews can only be created for verified transactions.")
        if self.reviewer_id and self.reviewee_id and self.reviewer_id == self.reviewee_id:
            raise ValidationError("Reviewer and reviewee must be different users.")
        if self.transaction_id and self.reviewer_id:
            if self.reviewer_id not in {self.transaction.buyer_id, self.transaction.seller_id}:
                raise ValidationError("Reviewer must be a participant in the transaction.")
        if self.transaction_id and self.reviewee_id:
            if self.reviewee_id not in {self.transaction.buyer_id, self.transaction.seller_id}:
                raise ValidationError("Reviewee must be a participant in the transaction.")
        if self.transaction_id and self.reviewer_id and self.reviewee_id:
            if self.reviewer_id == self.reviewee_id:
                raise ValidationError("Reviewer cannot review themselves.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
