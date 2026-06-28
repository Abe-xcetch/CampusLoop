from rest_framework import serializers
from core.users.infrastructure.orm_models import User, ReputationScore


class ReputationScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReputationScore
        fields = [
            "rating_average",
            "total_ratings_count",
            "completed_transactions_count",
            "is_trusted_seller",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    reputation = ReputationScoreSerializer(read_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "avatar_url",
            "phone_number",
            "role",
            "is_verified",
            "created_at",
            "reputation",
        ]
        read_only_fields = ["id", "email", "role", "is_verified", "created_at"]
