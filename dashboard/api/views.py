from datetime import date, timedelta
from random import Random

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dashboard.api.serializers import (
    DashboardWidgetSerializer,
    KeyboardShortcutSerializer,
)
from dashboard.models import DashboardWidget, KeyboardShortcut


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def widget_list(request):
    """Return all enabled dashboard widgets ordered by grid position."""
    widgets = DashboardWidget.objects.filter(enabled=True)
    serializer = DashboardWidgetSerializer(widgets, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def shortcut_list(request):
    """Return all enabled keyboard shortcuts."""
    shortcuts = KeyboardShortcut.objects.filter(enabled=True)
    serializer = KeyboardShortcutSerializer(shortcuts, many=True)
    return Response(serializer.data)


def _generate_time_series(base_value: float, volatility: float, days: int = 180):
    """Generate a mock daily price time series for the past N days."""
    today = date.today()
    dates = []
    prices = []
    price = base_value
    rng = Random(base_value)  # deterministic seed for reproducibility

    for i in range(days, 0, -1):
        day = today - timedelta(days=i)
        if day.weekday() >= 5:  # skip weekends
            continue
        change = rng.gauss(0, volatility)
        price = max(price * (1 + change), 0.01)
        dates.append(day.isoformat())
        prices.append(round(price, 4))

    return {"x": dates, "y": prices}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def gold_price(request):
    """Mock daily gold price data for the past 6 months."""
    return Response(_generate_time_series(base_value=1950.0, volatility=0.008))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def silver_price(request):
    """Mock daily silver price data for the past 6 months."""
    return Response(_generate_time_series(base_value=24.0, volatility=0.012))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def oil_price(request):
    """Mock daily WTI crude oil price data for the past 6 months."""
    return Response(_generate_time_series(base_value=78.0, volatility=0.015))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def treasury_10y(request):
    """Mock daily US 10-year Treasury yield data for the past 6 months."""
    return Response(_generate_time_series(base_value=4.25, volatility=0.005))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dow_gold_ratio(request):
    """Mock daily Dow Jones / Gold ratio data for the past 6 months."""
    return Response(_generate_time_series(base_value=18.5, volatility=0.007))
