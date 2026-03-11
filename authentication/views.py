"""Authentication views: login page and Google token endpoint."""

import json
import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


def login_view(request):
    """Render the login page with Google Identity Services button."""
    if request.user.is_authenticated:
        return redirect("/")

    if getattr(settings, "DEV_BYPASS_AUTH", False):
        from django.contrib.auth.models import User
        user, _ = User.objects.get_or_create(
            username="dev",
            defaults={"email": "dev@localhost", "is_staff": True, "is_superuser": True},
        )
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("/")

    return render(
        request,
        "authentication/login.html",
        {
            "google_client_id": settings.GOOGLE_CLIENT_ID,
        },
    )


@csrf_exempt
@require_http_methods(["POST"])
def google_auth(request):
    """Accept a Google ID token, verify it, and create a session."""
    try:
        body = json.loads(request.body)
        token = body.get("credential", "")
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

    user = authenticate(request, google_token=token)
    if user is None:
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=401)

    login(request, user, backend="authentication.backends.GoogleSingleUserBackend")
    return JsonResponse({"success": True})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Log the user out and redirect to login."""
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
