from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom Django ORM User model representing the 'User' database table.
    Uses Firebase UID as the username.
    """
    id = models.CharField(primary_key=True, max_length=128) # Firebase UID
    email = models.EmailField(unique=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[("STUDENT", "Student"), ("ADMIN", "Admin"), ("SUPERADMIN", "Super Admin")],
        default="STUDENT"
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.email} ({self.role})"


class Verification(models.Model):
    """
    Stores verification metadata for registration audits.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="verification")
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "verifications"


class ReputationScore(models.Model):
    """
    Aggregated seller scoring computed dynamically or updated post-transaction.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reputation")
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_ratings_count = models.IntegerField(default=0)
    completed_transactions_count = models.IntegerField(default=0)
    is_trusted_seller = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reputation_scores"

    def __str__(self):
        return f"{self.user.email} - Score: {self.rating_average}"
