from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from listings.models import Listing
from transactions.models import Transaction
from users.models import UUIDTimestampedModel


class FraudReportStatus(models.TextChoices):
    OPEN = "open", "Open"
    INVESTIGATING = "investigating", "Under Investigation"
    RESOLVED = "resolved", "Resolved"


class FraudReportReason(models.TextChoices):
    FRAUD_SCAM = "fraud_scam", "Scam/Fraudulent Activity"
    INAPPROPRIATE_CONTENT = "inappropriate_content", "Inappropriate Content"
    COUNTERFEIT = "counterfeit", "Counterfeit/Fake Product"
    SPAM = "spam", "Spam"
    OTHER = "other", "Other Policy Violation"


class FraudReport(UUIDTimestampedModel):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_filed",
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reports_against_user",
    )
    reported_listing = models.ForeignKey(
        Listing,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reports_against_listing",
    )
    reported_transaction = models.ForeignKey(
        Transaction,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reports_against_transaction",
    )
    reason = models.CharField(max_length=30, choices=FraudReportReason.choices)
    details = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=FraudReportStatus.choices,
        default=FraudReportStatus.OPEN,
    )
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="resolved_reports",
    )
    resolution_notes = models.TextField(blank=True)

    class Meta:
        db_table = "fraud_reports"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(reported_user__isnull=False)
                    | Q(reported_listing__isnull=False)
                    | Q(reported_transaction__isnull=False)
                ),
                name="fraud_report_requires_target",
            ),
        ]

    def __str__(self):
        return f"FraudReport {self.id} ({self.status})"

    def clean(self):
        super().clean()
        if not any([self.reported_user_id, self.reported_listing_id, self.reported_transaction_id]):
            raise ValidationError(
                "A fraud report must target a user, listing, or transaction."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
