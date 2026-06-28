from django.db import models
from django.conf import settings
from core.listings.infrastructure.orm_models import Listing


class FraudReport(models.Model):
    """
    Moderation request reports filed by users.
    """
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("INVESTIGATING", "Under Investigation"),
        ("RESOLVED", "Resolved"),
    ]

    REASON_CHOICES = [
        ("FRAUD_SCAM", "Scam/Fraudulent Listing"),
        ("INAPPROPRIATE_CONTENT", "Inappropriate Content"),
        ("COUNTERFEIT", "Counterfeit/Fake Product"),
        ("OUT_OF_STOCK_SPAM", "Spam/Sold Listing"),
        ("OTHER", "Other Policy Violation"),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_filed"
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reports_against"
    )
    reported_listing = models.ForeignKey(
        Listing,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reports_against"
    )
    
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="resolved_reports"
    )
    resolution_notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "fraud_reports"

    def __str__(self):
        target = f"Listing {self.reported_listing.id}" if self.reported_listing else f"User {self.reported_user.id}"
        return f"Report {self.id} against {target} ({self.status})"


class AdminAction(models.Model):
    """
    Audit log of administrative moderation actions.
    """
    ACTION_CHOICES = [
        ("APPROVE_LISTING", "Approve Listing"),
        ("REJECT_LISTING", "Reject Listing"),
        ("BAN_USER", "Ban User Account"),
        ("UNBAN_USER", "Unban User Account"),
        ("RESOLVE_REPORT", "Resolve Fraud Report"),
    ]

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="moderation_actions"
    )
    action_type = models.CharField(max_length=30, choices=ACTION_CHOICES)
    target_id = models.CharField(max_length=128) # UUID or identifier of target
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_actions"

    def __str__(self):
        return f"{self.admin.email} - {self.action_type} on {self.target_id}"
