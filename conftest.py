"""Pytest configuration and shared fixtures."""
import pytest
from django.test import Client


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def admin_user(db):
    """Create a superuser for testing."""
    from django.contrib.auth.models import User
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="testpass123",
    )


@pytest.fixture
def authenticated_client(client, admin_user):
    """Authenticated Django test client."""
    client.force_login(admin_user)
    return client
