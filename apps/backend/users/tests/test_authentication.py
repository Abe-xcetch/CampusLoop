from unittest.mock import patch

from django.test import RequestFactory, TestCase
from rest_framework import exceptions

from config.authentication import (
    ERROR_INVALID_TOKEN,
    ERROR_NON_STRATHMORE_EMAIL,
    ERROR_UNVERIFIED_EMAIL,
    FirebaseAuthentication,
)
from users.models import User


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
