"""Pytest configuration and shared fixtures."""
import pytest


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def admin_user(db):
    from django.contrib.auth.models import User
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="testpass123",
    )


@pytest.fixture
def authenticated_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client
