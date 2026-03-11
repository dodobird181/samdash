"""TDD: Tests for Google single-user authentication — written before implementation."""
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestGoogleBackend:
    def test_authenticate_valid_email(self):
        from authentication.backends import GoogleSingleUserBackend
        backend = GoogleSingleUserBackend()

        mock_payload = {"email": "test@example.com", "sub": "google-uid-123"}
        with patch("authentication.backends.settings.ALLOWED_GOOGLE_EMAIL", "test@example.com"):
            with patch("authentication.backends.id_token.verify_oauth2_token", return_value=mock_payload):
                user = backend.authenticate(request=None, google_token="fake-token")

        assert user is not None
        assert user.email == "test@example.com"

    def test_authenticate_wrong_email_rejected(self):
        from authentication.backends import GoogleSingleUserBackend
        backend = GoogleSingleUserBackend()

        mock_payload = {"email": "hacker@evil.com", "sub": "google-uid-456"}
        with patch("authentication.backends.settings.ALLOWED_GOOGLE_EMAIL", "allowed@example.com"):
            with patch("authentication.backends.id_token.verify_oauth2_token", return_value=mock_payload):
                user = backend.authenticate(request=None, google_token="fake-token")

        assert user is None

    def test_authenticate_invalid_token_returns_none(self):
        from authentication.backends import GoogleSingleUserBackend
        from google.auth.exceptions import GoogleAuthError
        backend = GoogleSingleUserBackend()

        with patch("authentication.backends.id_token.verify_oauth2_token", side_effect=ValueError("bad token")):
            user = backend.authenticate(request=None, google_token="bad-token")

        assert user is None

    def test_authenticate_creates_user_if_not_exists(self):
        from authentication.backends import GoogleSingleUserBackend
        backend = GoogleSingleUserBackend()

        mock_payload = {"email": "new@example.com", "sub": "google-uid-789", "name": "New User"}
        with patch("authentication.backends.settings.ALLOWED_GOOGLE_EMAIL", "new@example.com"):
            with patch("authentication.backends.id_token.verify_oauth2_token", return_value=mock_payload):
                user = backend.authenticate(request=None, google_token="fake-token")

        assert User.objects.filter(email="new@example.com").exists()

    def test_authenticate_reuses_existing_user(self):
        from authentication.backends import GoogleSingleUserBackend
        User.objects.create_user(username="existing", email="existing@example.com", password="x")
        backend = GoogleSingleUserBackend()

        mock_payload = {"email": "existing@example.com", "sub": "google-uid-000"}
        with patch("authentication.backends.settings.ALLOWED_GOOGLE_EMAIL", "existing@example.com"):
            with patch("authentication.backends.id_token.verify_oauth2_token", return_value=mock_payload):
                user = backend.authenticate(request=None, google_token="fake-token")

        assert User.objects.filter(email="existing@example.com").count() == 1
        assert user.email == "existing@example.com"


@pytest.mark.django_db
class TestLoginView:
    def test_login_page_accessible(self, client):
        response = client.get("/auth/login/")
        assert response.status_code == 200

    def test_dashboard_redirects_to_login_when_anonymous(self, client):
        response = client.get("/")
        assert response.status_code == 302
        assert "/auth/login/" in response["Location"]

    def test_google_token_login_valid(self, client):
        from django.contrib.auth.models import User
        mock_payload = {"email": "test@example.com", "sub": "google-uid-123"}
        with patch("authentication.backends.settings.ALLOWED_GOOGLE_EMAIL", "test@example.com"):
            with patch("authentication.backends.id_token.verify_oauth2_token", return_value=mock_payload):
                response = client.post("/auth/google/", {"credential": "fake-token"}, content_type="application/json")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_google_token_login_invalid(self, client):
        with patch("authentication.backends.id_token.verify_oauth2_token", side_effect=ValueError("bad")):
            response = client.post("/auth/google/", {"credential": "bad-token"}, content_type="application/json")
        assert response.status_code == 401
