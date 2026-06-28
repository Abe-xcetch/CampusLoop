import os

import firebase_admin
from firebase_admin import auth, credentials
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import authentication, exceptions

User = get_user_model()

# Initialize Firebase App globally
try:
    if settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred, {
            'storageBucket': settings.FIREBASE_STORAGE_BUCKET
        })
    else:
        # Fallback to default credentials environment variable resolution
        firebase_admin.initialize_app()
except Exception as e:
    # During testing or docker building, Firebase might fail to load. Log warning
    print(f"Warning: Firebase Admin SDK failed to initialize: {e}")


class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Custom Authentication Backend for Django REST Framework.
    
    Verifies the Firebase ID Token received in the 'Authorization: Bearer <token>' header.
    If the token is valid, returns the associated Django user.
    If the user does not exist locally, dynamically synchronizes their profile.
    """
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return None

        # Standard header format: 'Bearer <firebase_token>'
        parts = auth_header.split()
        if parts[0].lower() != "bearer":
            return None

        if len(parts) == 1:
            raise exceptions.AuthenticationFailed("Invalid token header. No credentials provided.")
        elif len(parts) > 2:
            raise exceptions.AuthenticationFailed("Invalid token header. Token string should not contain spaces.")

        id_token = parts[1]

        try:
            # Verify the token against Firebase. This checks signature, expiration, and project match.
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Invalid Firebase ID Token: {str(e)}")

        uid = decoded_token.get("uid")
        email = decoded_token.get("email", "")

        # Strict Security Rule: Registrations are locked to @strathmore.edu domains
        # (Though verified in the frontend, enforced here at the DB gateway)
        if not email.endswith(("@strathmore.edu", "@su.strathmore.edu", "@alumni.strathmore.edu")):
            raise exceptions.AuthenticationFailed(
                "Access Forbidden: Only Strathmore University email addresses are authorized."
            )

        # Map Firebase fields to Django User model
        name_parts = decoded_token.get("name", "").split(" ", 1)
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Fetch or register the user in Django DB
        user, created = User.objects.get_or_create(
            firebase_uid=uid,
            defaults={
                "username": uid,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
            },
        )

        # In a production DDD setup, we would publish a UserSyncedDomainEvent here
        # to trigger creation of empty ReputationScore or notification profiles asynchronously.

        return (user, None)
