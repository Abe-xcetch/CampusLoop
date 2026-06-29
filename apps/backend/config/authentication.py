import logging
import os

import firebase_admin
from django.conf import settings
from django.contrib.auth import get_user_model
from firebase_admin import auth, credentials
from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError, RevokedIdTokenError
from rest_framework import authentication, exceptions

logger = logging.getLogger(__name__)

User = get_user_model()

STRATHMORE_EMAIL_SUFFIX = "@strathmore.edu"

ERROR_INVALID_TOKEN = "Invalid or expired authentication token."
ERROR_UNVERIFIED_EMAIL = (
    "Email address is not verified. Please verify your Strathmore email before accessing CampusLoop."
)
ERROR_NON_STRATHMORE_EMAIL = (
    "Access denied. Only @strathmore.edu email addresses are allowed."
)
ERROR_MISSING_EMAIL = "Authentication token does not include an email address."


def _parse_bearer_token(auth_header: str) -> str:
    parts = auth_header.split()
    if parts[0].lower() != "bearer":
        raise exceptions.AuthenticationFailed(ERROR_INVALID_TOKEN)
    if len(parts) == 1:
        raise exceptions.AuthenticationFailed(ERROR_INVALID_TOKEN)
    if len(parts) > 2:
        raise exceptions.AuthenticationFailed(ERROR_INVALID_TOKEN)
    return parts[1]


def _verify_firebase_token(id_token: str) -> dict:
    try:
        from config.firebase import initialize_firebase
        initialize_firebase()
        return auth.verify_id_token(id_token)
    except (InvalidIdTokenError, ExpiredIdTokenError, RevokedIdTokenError):
        raise exceptions.AuthenticationFailed(ERROR_INVALID_TOKEN)
    except Exception as exc:
        logger.exception("Unexpected Firebase token verification error")
        raise exceptions.AuthenticationFailed(ERROR_INVALID_TOKEN) from exc


def _is_strathmore_email(email: str) -> bool:
    return email.lower().endswith(STRATHMORE_EMAIL_SUFFIX)


def _split_name(full_name: str) -> tuple[str, str]:
    name_parts = full_name.strip().split(" ", 1)
    first_name = name_parts[0] if name_parts else ""
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    return first_name, last_name


def _sync_local_user(
    *,
    firebase_uid: str,
    email: str,
    first_name: str,
    last_name: str,
    email_verified: bool,
) -> User:
    user = User.objects.filter(firebase_uid=firebase_uid).first()
    if user is None:
        user = User.objects.filter(email__iexact=email).first()

    if user is None:
        return User.objects.create(
            firebase_uid=firebase_uid,
            username=firebase_uid,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_verified=email_verified,
            is_active=True,
        )

    update_fields: list[str] = []
    if user.firebase_uid != firebase_uid:
        user.firebase_uid = firebase_uid
        update_fields.append("firebase_uid")
    if user.email != email:
        user.email = email
        update_fields.append("email")
    if user.first_name != first_name:
        user.first_name = first_name
        update_fields.append("first_name")
    if user.last_name != last_name:
        user.last_name = last_name
        update_fields.append("last_name")
    if user.is_verified != email_verified:
        user.is_verified = email_verified
        update_fields.append("is_verified")
    if not user.is_active:
        user.is_active = True
        update_fields.append("is_active")

    if update_fields:
        update_fields.append("updated_at")
        user.save(update_fields=update_fields)

    return user


class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Authenticate API requests using a Firebase ID token in the Authorization header.

    Header format: Authorization: Bearer <firebase_id_token>
    """

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return None

        id_token = _parse_bearer_token(auth_header)
        decoded_token = _verify_firebase_token(id_token)

        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email", "").strip()
        email_verified = bool(decoded_token.get("email_verified", False))
        full_name = decoded_token.get("name", "")

        if not firebase_uid:
            raise exceptions.AuthenticationFailed(ERROR_INVALID_TOKEN)
        if not email:
            raise exceptions.AuthenticationFailed(ERROR_MISSING_EMAIL)
        if not _is_strathmore_email(email):
            raise exceptions.AuthenticationFailed(ERROR_NON_STRATHMORE_EMAIL)
        if not email_verified:
            raise exceptions.AuthenticationFailed(ERROR_UNVERIFIED_EMAIL)

        first_name, last_name = _split_name(full_name)
        user = _sync_local_user(
            firebase_uid=firebase_uid,
            email=email,
            first_name=first_name,
            last_name=last_name,
            email_verified=email_verified,
        )

        return (user, decoded_token)
