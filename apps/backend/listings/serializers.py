from rest_framework import serializers
from listings.models import Category, Listing, ListingApproval, ListingApprovalStatus, ListingCondition


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "parent", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ListingSerializer(serializers.ModelSerializer):
    seller_email = serializers.EmailField(source="seller.email", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price",
            "condition",
            "approval_status",
            "category",
            "category_name",
            "seller",
            "seller_email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "seller", "approval_status", "created_at", "updated_at"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value

    def validate_approval_status(self, value):
        # Only admins can change approval status
        if self.instance and self.instance.approval_status != value:
            raise serializers.ValidationError(
                "Only admins can change approval status. Use the approval endpoint."
            )
        return value


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "condition", "category"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value


class ListingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "condition", "category"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value


class ListingApprovalSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)
    reviewed_by_email = serializers.EmailField(source="reviewed_by.email", read_only=True)

    class Meta:
        model = ListingApproval
        fields = [
            "id",
            "listing",
            "listing_title",
            "reviewed_by",
            "reviewed_by_email",
            "decision",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewed_by", "created_at", "updated_at"]


class ListingApprovalActionSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=[("approved", "Approved"), ("rejected", "Rejected")])
    notes = serializers.CharField(required=False, allow_blank=True)
