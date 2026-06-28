from unittest.mock import patch, MagicMock

from django.test import RequestFactory, TestCase
from rest_framework import exceptions
from rest_framework.test import APIClient

from config.authentication import (
    ERROR_INVALID_TOKEN,
    ERROR_NON_STRATHMORE_EMAIL,
    ERROR_UNVERIFIED_EMAIL,
    FirebaseAuthentication,
)
from users.models import User
from users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    PasswordResetView,
    ProtectedTestView,
)


class FirebaseAuthenticationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.auth = FirebaseAuthentication()

    def _request_with_token(self, token: str):
        return self.factory.get(
            "/api/v1/auth/me/",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

    @patch("config.authentication.auth.verify_id_token")
    def test_authenticates_verified_strathmore_user(self, mock_verify):
        mock_verify.return_value = {
            "uid": "firebase-uid-123",
            "email": "student@strathmore.edu",
            "email_verified": True,
            "name": "Jane Doe",
        }

        user, token = self.auth.authenticate(self._request_with_token("valid-token"))

        self.assertEqual(user.email, "student@strathmore.edu")
        self.assertEqual(user.firebase_uid, "firebase-uid-123")
        self.assertTrue(user.is_verified)
        self.assertEqual(token["uid"], "firebase-uid-123")

    @patch("config.authentication.auth.verify_id_token")
    def test_rejects_non_strathmore_email(self, mock_verify):
        mock_verify.return_value = {
            "uid": "firebase-uid-123",
            "email": "student@gmail.com",
            "email_verified": True,
            "name": "Jane Doe",
        }

        with self.assertRaisesMessage(exceptions.AuthenticationFailed, ERROR_NON_STRATHMORE_EMAIL):
            self.auth.authenticate(self._request_with_token("valid-token"))

    @patch("config.authentication.auth.verify_id_token")
    def test_rejects_unverified_email(self, mock_verify):
        mock_verify.return_value = {
            "uid": "firebase-uid-123",
            "email": "student@strathmore.edu",
            "email_verified": False,
            "name": "Jane Doe",
        }

        with self.assertRaisesMessage(exceptions.AuthenticationFailed, ERROR_UNVERIFIED_EMAIL):
            self.auth.authenticate(self._request_with_token("valid-token"))

    @patch("config.authentication.auth.verify_id_token")
    def test_rejects_invalid_token(self, mock_verify):
        from firebase_admin.auth import InvalidIdTokenError

        mock_verify.side_effect = InvalidIdTokenError("bad token")

        with self.assertRaisesMessage(exceptions.AuthenticationFailed, ERROR_INVALID_TOKEN):
            self.auth.authenticate(self._request_with_token("bad-token"))

    @patch("config.authentication.auth.verify_id_token")
    def test_syncs_existing_user_profile(self, mock_verify):
        existing = User.objects.create(
            firebase_uid="firebase-uid-123",
            username="firebase-uid-123",
            email="student@strathmore.edu",
            first_name="Old",
            last_name="Name",
            is_verified=False,
        )

        mock_verify.return_value = {
            "uid": "firebase-uid-123",
            "email": "student@strathmore.edu",
            "email_verified": True,
            "name": "Jane Doe",
        }

        user, _ = self.auth.authenticate(self._request_with_token("valid-token"))

        existing.refresh_from_db()
        self.assertEqual(user.id, existing.id)
        self.assertEqual(existing.first_name, "Jane")
        self.assertEqual(existing.last_name, "Doe")
        self.assertTrue(existing.is_verified)

    def test_returns_none_without_authorization_header(self):
        request = self.factory.get("/api/v1/auth/me/")
        self.assertIsNone(self.auth.authenticate(request))


class AuthEndpointTests(TestCase):
    """Tests for authentication API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()

    @patch("config.authentication.auth.verify_id_token")
    def test_register_with_valid_verified_strathmore_token(self, mock_verify):
        """Test registration with a valid verified Strathmore email token."""
        mock_verify.return_value = {
            "uid": "firebase-uid-new",
            "email": "newuser@strathmore.edu",
            "email_verified": True,
            "name": "John Smith",
        }

        response = self.client.post(
            "/api/v1/auth/register/", {"id_token": "valid-token"}
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], "newuser@strathmore.edu")
        self.assertTrue(User.objects.filter(email="newuser@strathmore.edu").exists())

    @patch("config.authentication.auth.verify_id_token")
    def test_register_rejects_non_strathmore_email(self, mock_verify):
        """Test registration rejects non-Strathmore email."""
        mock_verify.return_value = {
            "uid": "firebase-uid-123",
            "email": "user@gmail.com",
            "email_verified": True,
            "name": "Jane Doe",
        }

        response = self.client.post(
            "/api/v1/auth/register/", {"id_token": "valid-token"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.data)
        self.assertIn("@strathmore.edu", response.data["detail"])

    @patch("config.authentication.auth.verify_id_token")
    def test_register_rejects_unverified_email(self, mock_verify):
        """Test registration rejects unverified Firebase email."""
        mock_verify.return_value = {
            "uid": "firebase-uid-123",
            "email": "student@strathmore.edu",
            "email_verified": False,
            "name": "Jane Doe",
        }

        response = self.client.post(
            "/api/v1/auth/register/", {"id_token": "valid-token"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.data)
        self.assertIn("not verified", response.data["detail"])

    @patch("config.authentication.auth.verify_id_token")
    def test_register_updates_existing_user(self, mock_verify):
        """Test registration updates existing user profile."""
        existing = User.objects.create(
            firebase_uid="firebase-uid-existing",
            username="firebase-uid-existing",
            email="existing@strathmore.edu",
            first_name="Old",
            last_name="Name",
            is_verified=False,
        )

        mock_verify.return_value = {
            "uid": "firebase-uid-existing",
            "email": "existing@strathmore.edu",
            "email_verified": True,
            "name": "Updated Name",
        }

        response = self.client.post(
            "/api/v1/auth/register/", {"id_token": "valid-token"}
        )

        self.assertEqual(response.status_code, 201)
        existing.refresh_from_db()
        self.assertEqual(existing.first_name, "Updated")
        self.assertEqual(existing.last_name, "Name")
        self.assertTrue(existing.is_verified)

    @patch("config.authentication.auth.verify_id_token")
    def test_login_with_valid_token(self, mock_verify):
        """Test login with valid Firebase token."""
        mock_verify.return_value = {
            "uid": "firebase-uid-login",
            "email": "loginuser@strathmore.edu",
            "email_verified": True,
            "name": "Login User",
        }

        response = self.client.post(
            "/api/v1/auth/login/", {"id_token": "valid-token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "loginuser@strathmore.edu")

    @patch("config.authentication.auth.verify_id_token")
    def test_login_rejects_invalid_token(self, mock_verify):
        """Test login rejects invalid token."""
        from firebase_admin.auth import InvalidIdTokenError

        mock_verify.side_effect = InvalidIdTokenError("bad token")

        response = self.client.post(
            "/api/v1/auth/login/", {"id_token": "bad-token"}
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.data)

    @patch("config.authentication.auth.verify_id_token")
    def test_me_endpoint_requires_authentication(self, mock_verify):
        """Test /me/ endpoint requires authentication."""
        response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(response.status_code, 401)

    @patch("config.authentication.auth.verify_id_token")
    def test_me_endpoint_returns_user_profile(self, mock_verify):
        """Test /me/ endpoint returns authenticated user profile."""
        mock_verify.return_value = {
            "uid": "firebase-uid-me",
            "email": "meuser@strathmore.edu",
            "email_verified": True,
            "name": "Me User",
        }

        # First authenticate by calling login
        self.client.post("/api/v1/auth/login/", {"id_token": "valid-token"})

        # Now call me with the same token
        response = self.client.get(
            "/api/v1/auth/me/",
            HTTP_AUTHORIZATION="Bearer valid-token"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "meuser@strathmore.edu")

    @patch("config.authentication.auth.verify_id_token")
    def test_logout_requires_authentication(self, mock_verify):
        """Test logout endpoint requires authentication."""
        response = self.client.post("/api/v1/auth/logout/")
        self.assertEqual(response.status_code, 401)

    @patch("config.authentication.auth.verify_id_token")
    def test_logout_returns_success_message(self, mock_verify):
        """Test logout returns success message."""
        mock_verify.return_value = {
            "uid": "firebase-uid-logout",
            "email": "logoutuser@strathmore.edu",
            "email_verified": True,
            "name": "Logout User",
        }

        response = self.client.post(
            "/api/v1/auth/logout/",
            HTTP_AUTHORIZATION="Bearer valid-token"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("detail", response.data)
        self.assertIn("logged out", response.data["detail"].lower())

    def test_password_reset_validates_strathmore_domain(self):
        """Test password reset validates @strathmore.edu domain."""
        response = self.client.post(
            "/api/v1/auth/password-reset/", {"email": "user@gmail.com"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.data)
        self.assertIn("@strathmore.edu", response.data["detail"])

    def test_password_reset_returns_safe_message(self):
        """Test password reset returns safe message that doesn't expose email existence."""
        response = self.client.post(
            "/api/v1/auth/password-reset/", {"email": "nonexistent@strathmore.edu"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("detail", response.data)
        # Should not reveal whether email exists
        self.assertIn("If an account", response.data["detail"])

    @patch("config.authentication.auth.verify_id_token")
    def test_protected_endpoint_requires_authentication(self, mock_verify):
        """Test protected-test endpoint requires authentication."""
        response = self.client.get("/api/v1/auth/protected-test/")
        self.assertEqual(response.status_code, 401)

    @patch("config.authentication.auth.verify_id_token")
    def test_protected_endpoint_accessible_when_authenticated(self, mock_verify):
        """Test protected-test endpoint is accessible when authenticated."""
        mock_verify.return_value = {
            "uid": "firebase-uid-protected",
            "email": "protected@strathmore.edu",
            "email_verified": True,
            "name": "Protected User",
        }

        response = self.client.get(
            "/api/v1/auth/protected-test/",
            HTTP_AUTHORIZATION="Bearer valid-token"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("detail", response.data)
        self.assertIn("successfully accessed", response.data["detail"].lower())
        self.assertEqual(response.data["user"], "protected@strathmore.edu")
