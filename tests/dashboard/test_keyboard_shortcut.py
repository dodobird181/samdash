"""TDD: Tests for KeyboardShortcut model — written before implementation."""

import pytest


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
