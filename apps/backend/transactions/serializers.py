from rest_framework import serializers
from transactions.models import Transaction, Review, TransactionStatus
from listings.models import Listing, ListingApprovalStatus


class TransactionSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)
    listing_price = serializers.DecimalField(source="listing.price", max_digits=10, decimal_places=2, read_only=True)
    buyer_email = serializers.EmailField(source="buyer.email", read_only=True)
    seller_email = serializers.EmailField(source="seller.email", read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            "id",
            "listing",
            "listing_title",
            "listing_price",
            "buyer",
            "buyer_email",
            "seller",
            "seller_email",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "buyer", "seller", "status", "created_at", "updated_at"]


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["listing"]


class TransactionStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=TransactionStatus.choices)


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_email = serializers.EmailField(source="reviewer.email", read_only=True)
    reviewee_email = serializers.EmailField(source="reviewee.email", read_only=True)
    transaction_status = serializers.CharField(source="transaction.status", read_only=True)
    
    class Meta:
        model = Review
        fields = [
            "id",
            "transaction",
            "transaction_status",
            "reviewer",
            "reviewer_email",
            "reviewee",
            "reviewee_email",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "transaction", "reviewer", "created_at", "updated_at"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["reviewee", "rating", "comment"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_reviewee(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("You cannot review yourself.")
        return value
