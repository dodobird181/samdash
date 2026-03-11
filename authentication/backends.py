"""Google single-user authentication backend."""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

logger = logging.getLogger(__name__)


class GoogleSingleUserBackend:
    """
    Authenticate via Google Identity Services token.
    Only the single configured ALLOWED_GOOGLE_EMAIL is permitted.
    """

    def authenticate(self, request, google_token=None, **kwargs):
        if not google_token:
            return None

        try:
            payload = id_token.verify_oauth2_token(
                google_token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
        except (ValueError, Exception) as exc:
            logger.warning("Google token verification failed: %s", exc)
            return None

        email = payload.get("email", "")
        if email != settings.ALLOWED_GOOGLE_EMAIL:
            logger.warning("Rejected login attempt from: %s", email)
            return None

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0]},
        )
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
