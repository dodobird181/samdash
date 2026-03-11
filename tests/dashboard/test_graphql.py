"""Tests for Dashboard GraphQL API."""

import pytest
from graphene.test import Client
from config.schema import schema


@pytest.mark.django_db
class TestDashboardGraphQL:
    def test_widgets_query_requires_auth(self):
        """Test that widgets query requires authentication."""
        from django.contrib.auth.models import AnonymousUser

        query = """
            query {
                widgets {
                    id
                    title
                    widgetType
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": AnonymousUser()})()
        result = client.execute(query, context_value=mock_request)
        # Should return empty list when not authenticated
        assert result["data"]["widgets"] == []

    def test_widgets_query_authenticated(self, admin_user):
        """Test widgets query returns data when authenticated."""
        from dashboard.models import DashboardWidget

        DashboardWidget.objects.create(
            title="Gold",
            widget_type="gold_price",
            api_endpoint="/api/gold-price/",
            enabled=True,
        )

        query = """
            query {
                widgets {
                    id
                    title
                    widgetType
                    apiEndpoint
                    gridX
                    gridY
                    width
                    height
                    refreshIntervalSeconds
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": admin_user})()
        result = client.execute(query, context_value=mock_request)

        assert "errors" not in result
        assert len(result["data"]["widgets"]) == 1
        assert result["data"]["widgets"][0]["title"] == "Gold"

    def test_only_enabled_widgets_returned(self, admin_user):
        """Test that only enabled widgets are returned."""
        from dashboard.models import DashboardWidget

        DashboardWidget.objects.create(
            title="On", widget_type="gold_price", api_endpoint="/a/", enabled=True
        )
        DashboardWidget.objects.create(
            title="Off", widget_type="silver_price", api_endpoint="/b/", enabled=False
        )

        query = """
            query {
                widgets {
                    title
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": admin_user})()
        result = client.execute(query, context_value=mock_request)

        titles = [w["title"] for w in result["data"]["widgets"]]
        assert "On" in titles
        assert "Off" not in titles

    def test_shortcuts_query_authenticated(self, admin_user):
        """Test shortcuts query returns data when authenticated."""
        from dashboard.models import KeyboardShortcut

        KeyboardShortcut.objects.create(
            key="g", description="Focus gold", action_type="focus_widget", enabled=True
        )

        query = """
            query {
                shortcuts {
                    id
                    key
                    description
                    actionType
                    targetWidget
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": admin_user})()
        result = client.execute(query, context_value=mock_request)

        assert "errors" not in result
        assert len(result["data"]["shortcuts"]) == 1
        assert result["data"]["shortcuts"][0]["key"] == "g"

    def test_gold_price_query_authenticated(self, admin_user):
        """Test gold price query returns time series data."""
        query = """
            query {
                goldPrice {
                    x
                    y
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": admin_user})()
        result = client.execute(query, context_value=mock_request)

        assert "errors" not in result
        assert "goldPrice" in result["data"]
        assert "x" in result["data"]["goldPrice"]
        assert "y" in result["data"]["goldPrice"]
        assert len(result["data"]["goldPrice"]["x"]) > 0
        assert len(result["data"]["goldPrice"]["y"]) > 0

    def test_market_data_queries(self, admin_user):
        """Test all market data queries return time series data."""
        queries = [
            "silverPrice",
            "oilPrice",
            "treasury10y",
            "dowGoldRatio",
        ]

        for query_name in queries:
            query = f"""
                query {{
                    {query_name} {{
                        x
                        y
                    }}
                }}
            """
            client = Client(schema)
            mock_request = type("Request", (), {"user": admin_user})()
            result = client.execute(query, context_value=mock_request)

            assert "errors" not in result, f"Error in {query_name}: {result.get('errors')}"
            assert query_name in result["data"]
            assert result["data"][query_name] is not None
            assert len(result["data"][query_name]["x"]) > 0
