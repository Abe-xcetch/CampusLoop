from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Stores platform notifications dispatched to users.
    """
    TYPE_CHOICES = [
        ("TRANSACTION_UPDATE", "Transaction Status Update"),
        ("NEW_REVIEW", "New Review Received"),
        ("LISTING_APPROVED", "Listing Approved by Admin"),
        ("REPORT_ALERT", "Fraud Report Alert"),
        ("GENERAL", "General Notification"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    title = models.CharField(max_length=150)
    body = models.TextField()
    type = models.CharField(max_length=35, choices=TYPE_CHOICES, default="GENERAL")
    is_read = models.BooleanField(default=False)
    redirect_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification {self.id} for {self.user.email} (Read: {self.is_read})"
