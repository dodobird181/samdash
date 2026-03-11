"""GraphQL schema for dashboard app."""

import graphene
from graphene_django import DjangoObjectType

from dashboard.models import DashboardWidget, KeyboardShortcut
from dashboard.utils import generate_time_series


class DashboardWidgetType(DjangoObjectType):
    """GraphQL type for DashboardWidget model."""

    class Meta:
        model = DashboardWidget
        fields = (
            "id",
            "title",
            "widget_type",
            "api_endpoint",
            "grid_x",
            "grid_y",
            "width",
            "height",
            "enabled",
            "refresh_interval_seconds",
        )


class KeyboardShortcutType(DjangoObjectType):
    """GraphQL type for KeyboardShortcut model."""

    class Meta:
        model = KeyboardShortcut
        fields = ("id", "key", "description", "action_type", "target_widget", "enabled")


class TimeSeriesDataType(graphene.ObjectType):
    """Time series data with x (dates) and y (values) arrays."""

    x = graphene.List(graphene.String)
    y = graphene.List(graphene.Float)


class Query(graphene.ObjectType):
    """Dashboard GraphQL queries."""

    widgets = graphene.List(DashboardWidgetType)
    shortcuts = graphene.List(KeyboardShortcutType)
    gold_price = graphene.Field(TimeSeriesDataType)
    silver_price = graphene.Field(TimeSeriesDataType)
    oil_price = graphene.Field(TimeSeriesDataType)
    treasury_10y = graphene.Field(TimeSeriesDataType)
    dow_gold_ratio = graphene.Field(TimeSeriesDataType)

    def resolve_widgets(self, info):
        """Return all enabled dashboard widgets ordered by grid position."""
        user = info.context.user
        if not user.is_authenticated:
            return []
        return DashboardWidget.objects.filter(enabled=True)

    def resolve_shortcuts(self, info):
        """Return all enabled keyboard shortcuts."""
        user = info.context.user
        if not user.is_authenticated:
            return []
        return KeyboardShortcut.objects.filter(enabled=True)

    def resolve_gold_price(self, info):
        """Mock daily gold price data for the past 6 months."""
        user = info.context.user
        if not user.is_authenticated:
            return None
        data = generate_time_series(base_value=1950.0, volatility=0.008)
        return TimeSeriesDataType(x=data["x"], y=data["y"])

    def resolve_silver_price(self, info):
        """Mock daily silver price data for the past 6 months."""
        user = info.context.user
        if not user.is_authenticated:
            return None
        data = generate_time_series(base_value=24.0, volatility=0.012)
        return TimeSeriesDataType(x=data["x"], y=data["y"])

    def resolve_oil_price(self, info):
        """Mock daily WTI crude oil price data for the past 6 months."""
        user = info.context.user
        if not user.is_authenticated:
            return None
        data = generate_time_series(base_value=78.0, volatility=0.015)
        return TimeSeriesDataType(x=data["x"], y=data["y"])

    def resolve_treasury_10y(self, info):
        """Mock daily US 10-year Treasury yield data for the past 6 months."""
        user = info.context.user
        if not user.is_authenticated:
            return None
        data = generate_time_series(base_value=4.25, volatility=0.005)
        return TimeSeriesDataType(x=data["x"], y=data["y"])

    def resolve_dow_gold_ratio(self, info):
        """Mock daily Dow Jones / Gold ratio data for the past 6 months."""
        user = info.context.user
        if not user.is_authenticated:
            return None
        data = generate_time_series(base_value=18.5, volatility=0.007)
        return TimeSeriesDataType(x=data["x"], y=data["y"])


schema = graphene.Schema(query=Query)
