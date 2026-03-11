"""TDD: Tests for dashboard models — written before implementation."""

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


@pytest.mark.django_db
class TestKeyboardShortcut:
    def test_create_shortcut(self):
        from dashboard.models import KeyboardShortcut

        s = KeyboardShortcut.objects.create(
            key="g",
            description="Focus gold widget",
            action_type="focus_widget",
            target_widget="gold_price",
            enabled=True,
        )
        assert s.pk is not None
        assert s.key == "g"

    def test_shortcut_str(self):
        from dashboard.models import KeyboardShortcut

        s = KeyboardShortcut(key="g", description="Focus gold")
        assert "g" in str(s)

    def test_shortcut_defaults(self):
        from dashboard.models import KeyboardShortcut

        s = KeyboardShortcut.objects.create(
            key="n",
            description="Next widget",
            action_type="next_widget",
        )
        assert s.enabled is True
        assert s.target_widget == ""

    def test_action_type_choices(self):
        from dashboard.models import KeyboardShortcut

        valid_types = [
            "focus_widget",
            "expand_widget",
            "refresh_widget",
            "next_widget",
            "previous_widget",
        ]
        for action in valid_types:
            s = KeyboardShortcut(key="x", description="test", action_type=action)
            s.full_clean()  # must not raise

    def test_only_enabled_shortcuts(self):
        from dashboard.models import KeyboardShortcut

        KeyboardShortcut.objects.create(key="a", description="A", action_type="next_widget", enabled=True)
        KeyboardShortcut.objects.create(key="b", description="B", action_type="next_widget", enabled=False)
        assert KeyboardShortcut.objects.filter(enabled=True).count() == 1
