from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Hierarchical listing categories.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subcategories"
    )

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Listing(models.Model):
    """
    Marketplace Listings ORM Model.
    """
    CONDITION_CHOICES = [
        ("NEW", "New"),
        ("LIKE_NEW", "Like New"),
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
    ]

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("PENDING_APPROVAL", "Pending Admin Approval"),
        ("ACTIVE", "Active"),
        ("SOLD", "Sold"),
        ("FLAGGED", "Flagged"),
        ("ARCHIVED", "Archived"),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=15, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING_APPROVAL")
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="listings")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="approved_listings"
    )

    class Meta:
        db_table = "listings"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.price} KES"


class ListingMedia(models.Model):
    """
    Media attachments linked to listings, pointing to Firebase Storage bucket paths.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="media")
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "listing_media"
