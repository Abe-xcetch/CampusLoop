from django.conf import settings
from django.db import models

from users.models import UUIDTimestampedModel


class AdminActionType(models.TextChoices):
    APPROVE_LISTING = "approve_listing", "Approve Listing"
    REJECT_LISTING = "reject_listing", "Reject Listing"
    BAN_USER = "ban_user", "Ban User"
    UNBAN_USER = "unban_user", "Unban User"
    RESOLVE_REPORT = "resolve_report", "Resolve Fraud Report"
    VERIFY_TRANSACTION = "verify_transaction", "Verify Transaction"


class AdminAction(UUIDTimestampedModel):
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_actions",
    )
    action_type = models.CharField(max_length=30, choices=AdminActionType.choices)
    target_id = models.UUIDField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "admin_actions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["action_type"]),
            models.Index(fields=["target_id"]),
        ]

    def __str__(self):
        return f"{self.admin.email} - {self.action_type}"
