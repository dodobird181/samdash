"""Main dashboard view."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.models import DashboardWidget


@login_required
def dashboard(request):
    """Render the main dashboard. Widgets are loaded client-side via the API."""
    widgets = DashboardWidget.objects.filter(enabled=True)
    return render(request, "dashboard/dashboard.html", {"widgets": widgets})
