"""TDD: Tests for DashboardWidget model — written before implementation."""

import pytest


@pytest.mark.django_db
class TestDashboardWidget:
    def test_create_widget(self):
        from dashboard.models import DashboardWidget

        w = DashboardWidget.objects.create(
            title="Gold Price",
            widget_type="gold_price",
            api_endpoint="/api/gold-price/",
            grid_x=0,
            grid_y=0,
            width=1,
            height=1,
            enabled=True,
            refresh_interval_seconds=60,
        )
        assert w.pk is not None
        assert w.title == "Gold Price"
        assert w.enabled is True

    def test_widget_str(self):
        from dashboard.models import DashboardWidget

        w = DashboardWidget(title="Gold Price", widget_type="gold_price")
        assert "Gold Price" in str(w)

    def test_widget_defaults(self):
        from dashboard.models import DashboardWidget

        w = DashboardWidget.objects.create(
            title="Test",
            widget_type="gold_price",
            api_endpoint="/api/gold-price/",
        )
        assert w.enabled is True
        assert w.grid_x == 0
        assert w.grid_y == 0
        assert w.width == 1
        assert w.height == 1
        assert w.refresh_interval_seconds == 300

    def test_disabled_widget(self):
        from dashboard.models import DashboardWidget

        w = DashboardWidget.objects.create(
            title="Disabled",
            widget_type="gold_price",
            api_endpoint="/api/gold-price/",
            enabled=False,
        )
        assert w.enabled is False

    def test_enabled_filter(self):
        from dashboard.models import DashboardWidget

        DashboardWidget.objects.create(title="On", widget_type="gold_price", api_endpoint="/a/", enabled=True)
        DashboardWidget.objects.create(title="Off", widget_type="silver_price", api_endpoint="/b/", enabled=False)
        enabled = DashboardWidget.objects.filter(enabled=True)
        assert enabled.count() == 1
        assert enabled.first().title == "On"

    def test_ordering_by_position(self):
        from dashboard.models import DashboardWidget

        DashboardWidget.objects.create(title="B", widget_type="gold_price", api_endpoint="/b/", grid_y=1, grid_x=0)
        DashboardWidget.objects.create(
            title="A", widget_type="silver_price", api_endpoint="/a/", grid_y=0, grid_x=0
        )
        widgets = list(DashboardWidget.objects.all())
        assert widgets[0].title == "A"
        assert widgets[1].title == "B"
