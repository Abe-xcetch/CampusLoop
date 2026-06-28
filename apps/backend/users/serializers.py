from rest_framework import serializers

from users.models import User


class AuthenticatedUserSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = fields
