from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import Serializer, CharField

from users.serializers import AuthenticatedUserSerializer
from config.authentication import (
    _verify_firebase_token,
    _is_strathmore_email,
    _split_name,
    _sync_local_user,
    ERROR_INVALID_TOKEN,
    ERROR_UNVERIFIED_EMAIL,
    ERROR_NON_STRATHMORE_EMAIL,
    ERROR_MISSING_EMAIL,
)
from users.models import User


class AuthMeView(APIView):
    """
    GET /api/v1/auth/me/

    Protected endpoint that returns the current authenticated user profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AuthenticatedUserSerializer(request.user)
        return Response(serializer.data)


class RegisterView(APIView):
    """
    POST /api/v1/auth/register/

    Accepts Firebase ID token, verifies it, and creates or updates local User profile.
    Rejects non-@strathmore.edu emails and unverified Firebase emails.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    class RegisterSerializer(Serializer):
        id_token = CharField(required=True)

    def post(self, request):
        serializer = self.RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        id_token = serializer.validated_data["id_token"]

        try:
            decoded_token = _verify_firebase_token(id_token)
        except Exception:
            return Response(
                {"detail": ERROR_INVALID_TOKEN},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email", "").strip()
        email_verified = bool(decoded_token.get("email_verified", False))
        full_name = decoded_token.get("name", "")

        if not firebase_uid:
            return Response(
                {"detail": ERROR_INVALID_TOKEN},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not email:
            return Response(
                {"detail": ERROR_MISSING_EMAIL},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not _is_strathmore_email(email):
            return Response(
                {"detail": ERROR_NON_STRATHMORE_EMAIL},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not email_verified:
            return Response(
                {"detail": ERROR_UNVERIFIED_EMAIL},
                status=status.HTTP_403_FORBIDDEN,
            )

        first_name, last_name = _split_name(full_name)
        user = _sync_local_user(
            firebase_uid=firebase_uid,
            email=email,
            first_name=first_name,
            last_name=last_name,
            email_verified=email_verified,
        )

        response_serializer = AuthenticatedUserSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    POST /api/v1/auth/login/

    Accepts Firebase ID token, verifies it, and returns local authenticated user profile.
    Does not create password-based login because Firebase handles authentication.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    class LoginSerializer(Serializer):
        id_token = CharField(required=True)

    def post(self, request):
        serializer = self.LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        id_token = serializer.validated_data["id_token"]

        try:
            decoded_token = _verify_firebase_token(id_token)
        except Exception:
            return Response(
                {"detail": ERROR_INVALID_TOKEN},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email", "").strip()
        email_verified = bool(decoded_token.get("email_verified", False))
        full_name = decoded_token.get("name", "")

        if not firebase_uid:
            return Response(
                {"detail": ERROR_INVALID_TOKEN},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not email:
            return Response(
                {"detail": ERROR_MISSING_EMAIL},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not _is_strathmore_email(email):
            return Response(
                {"detail": ERROR_NON_STRATHMORE_EMAIL},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not email_verified:
            return Response(
                {"detail": ERROR_UNVERIFIED_EMAIL},
                status=status.HTTP_403_FORBIDDEN,
            )

        first_name, last_name = _split_name(full_name)
        user = _sync_local_user(
            firebase_uid=firebase_uid,
            email=email,
            first_name=first_name,
            last_name=last_name,
            email_verified=email_verified,
        )

        response_serializer = AuthenticatedUserSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/

    Protected endpoint that returns logout success message.
    Frontend/mobile must delete stored token on logout.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"detail": "Successfully logged out. Please delete your stored Firebase token."},
            status=status.HTTP_200_OK,
        )


class PasswordResetView(APIView):
    """
    POST /api/v1/auth/password-reset/

    Accepts email, validates @strathmore.edu domain, and returns a safe success message.
    Does not expose whether the email exists.
    Firebase handles password reset emails.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    class PasswordResetSerializer(Serializer):
        email = CharField(required=True)

    def post(self, request):
        serializer = self.PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"].strip().lower()

        if not _is_strathmore_email(email):
            return Response(
                {"detail": "Only @strathmore.edu email addresses are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Firebase password reset can be integrated here
        # For now, return a safe message that doesn't expose email existence
        return Response(
            {
                "detail": "If an account with this email exists, a password reset link will be sent via Firebase."
            },
            status=status.HTTP_200_OK,
        )


class ProtectedTestView(APIView):
    """
    GET /api/v1/auth/protected-test/

    Protected endpoint used to demonstrate that unauthenticated users cannot access protected API routes.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "detail": "You have successfully accessed a protected endpoint.",
                "user": request.user.email,
            },
            status=status.HTTP_200_OK,
        )
