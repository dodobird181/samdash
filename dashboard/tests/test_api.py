"""TDD: Tests for dashboard API endpoints — written before implementation."""
import pytest


@pytest.mark.django_db
class TestWidgetAPI:
    def test_list_widgets_requires_auth(self, api_client):
        response = api_client.get("/api/widgets/")
        assert response.status_code == 403

    def test_list_widgets_authenticated(self, authenticated_client):
        from dashboard.models import DashboardWidget
        DashboardWidget.objects.create(
            title="Gold", widget_type="gold_price", api_endpoint="/api/gold-price/", enabled=True
        )
        response = authenticated_client.get("/api/widgets/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Gold"

    def test_only_enabled_widgets_returned(self, authenticated_client):
        from dashboard.models import DashboardWidget
        DashboardWidget.objects.create(title="On", widget_type="gold_price", api_endpoint="/a/", enabled=True)
        DashboardWidget.objects.create(title="Off", widget_type="silver_price", api_endpoint="/b/", enabled=False)
        response = authenticated_client.get("/api/widgets/")
        assert response.status_code == 200
        titles = [w["title"] for w in response.json()]
        assert "On" in titles
        assert "Off" not in titles

    def test_widget_response_shape(self, authenticated_client):
        from dashboard.models import DashboardWidget
        DashboardWidget.objects.create(
            title="Gold", widget_type="gold_price", api_endpoint="/api/gold-price/",
            grid_x=0, grid_y=0, width=2, height=2, enabled=True, refresh_interval_seconds=60
        )
        response = authenticated_client.get("/api/widgets/")
        w = response.json()[0]
        for field in ["id", "title", "widget_type", "api_endpoint", "grid_x", "grid_y", "width", "height", "refresh_interval_seconds"]:
            assert field in w, f"Missing field: {field}"


@pytest.mark.django_db
class TestShortcutsAPI:
    def test_list_shortcuts_requires_auth(self, api_client):
        response = api_client.get("/api/shortcuts/")
        assert response.status_code == 403

    def test_list_shortcuts_authenticated(self, authenticated_client):
        from dashboard.models import KeyboardShortcut
        KeyboardShortcut.objects.create(key="g", description="Focus gold", action_type="focus_widget", enabled=True)
        response = authenticated_client.get("/api/shortcuts/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["key"] == "g"

    def test_only_enabled_shortcuts_returned(self, authenticated_client):
        from dashboard.models import KeyboardShortcut
        KeyboardShortcut.objects.create(key="a", description="A", action_type="next_widget", enabled=True)
        KeyboardShortcut.objects.create(key="b", description="B", action_type="next_widget", enabled=False)
        response = authenticated_client.get("/api/shortcuts/")
        keys = [s["key"] for s in response.json()]
        assert "a" in keys
        assert "b" not in keys

    def test_shortcut_response_shape(self, authenticated_client):
        from dashboard.models import KeyboardShortcut
        KeyboardShortcut.objects.create(key="g", description="Focus gold", action_type="focus_widget")
        response = authenticated_client.get("/api/shortcuts/")
        s = response.json()[0]
        for field in ["id", "key", "description", "action_type", "target_widget"]:
            assert field in s, f"Missing field: {field}"


@pytest.mark.django_db
class TestMarketDataAPIs:
    def test_gold_price_requires_auth(self, api_client):
        response = api_client.get("/api/gold-price/")
        assert response.status_code == 403

    def test_gold_price_returns_data(self, authenticated_client):
        response = authenticated_client.get("/api/gold-price/")
        assert response.status_code == 200
        data = response.json()
        assert "x" in data
        assert "y" in data
        assert len(data["x"]) == len(data["y"])
        assert len(data["x"]) > 0

    def test_silver_price_returns_data(self, authenticated_client):
        response = authenticated_client.get("/api/silver-price/")
        assert response.status_code == 200
        data = response.json()
        assert "x" in data and "y" in data

    def test_oil_price_returns_data(self, authenticated_client):
        response = authenticated_client.get("/api/oil-price/")
        assert response.status_code == 200
        data = response.json()
        assert "x" in data and "y" in data

    def test_treasury_10y_returns_data(self, authenticated_client):
        response = authenticated_client.get("/api/treasury-10y/")
        assert response.status_code == 200
        data = response.json()
        assert "x" in data and "y" in data

    def test_dow_gold_ratio_returns_data(self, authenticated_client):
        response = authenticated_client.get("/api/dow-gold-ratio/")
        assert response.status_code == 200
        data = response.json()
        assert "x" in data and "y" in data

    def test_gold_price_has_180_days(self, authenticated_client):
        response = authenticated_client.get("/api/gold-price/")
        data = response.json()
        # 6 months of daily bars (weekdays only) is roughly 130+ data points
        assert len(data["x"]) >= 100

    def test_silver_price_has_180_days(self, authenticated_client):
        response = authenticated_client.get("/api/silver-price/")
        data = response.json()
        assert len(data["x"]) >= 100
