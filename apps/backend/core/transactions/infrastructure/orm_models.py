from django.db import models
from django.conf import settings
from core.listings.infrastructure.orm_models import Listing


class Transaction(models.Model):
    """
    Tracks peer-to-peer exchange states.
    """
    STATUS_CHOICES = [
        ("INITIATED", "Initiated"),
        ("CONFIRMED", "Seller Confirmed"),
        ("COMPLETED", "Buyer Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="transactions")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sales")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="INITIATED")
    
    initiated_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "transactions"

    def __str__(self):
        return f"Tx {self.id}: {self.listing.title} ({self.status})"


class Review(models.Model):
    """
    Transaction-verified peer review structure.
    Reviews are ONLY valid if linked to a COMPLETED transaction.
    """
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="review")
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_given"
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_received"
    )
    
    rating = models.IntegerField()  # 1 to 5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews"
        # Ensure a reviewer can't review the same transaction twice
        unique_together = ("transaction", "reviewer")

    def __str__(self):
        return f"Review {self.id} (Rating: {self.rating})"
