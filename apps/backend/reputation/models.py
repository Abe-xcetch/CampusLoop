from django.conf import settings
from django.db import models

from users.models import UUIDTimestampedModel


class ReputationScore(UUIDTimestampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reputation",
    )
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ratings_count = models.PositiveIntegerField(default=0)
    completed_transactions_count = models.PositiveIntegerField(default=0)
    is_trusted_seller = models.BooleanField(default=False)

    class Meta:
        db_table = "reputation_scores"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.email} - {self.rating_average}"
